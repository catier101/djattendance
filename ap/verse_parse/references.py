# adapted from python-scriptures

import re
import urllib2
import json

from bible_re import get_book

class InvalidReferenceException(Exception):
    """
    Invalid Reference Exception
    """
    pass


def is_valid_reference(bookname, chapter, verse=None,
                                 end_chapter=None, end_verse=None, more_verses=None):
    """
    Check to see if a scripture reference is valid
    """
    try:
        return normalize_reference(bookname, chapter, verse,
            end_chapter, end_verse) is not None
    except InvalidReferenceException:
        return False

def reference_to_string(ref):
    '''
    Takes tupled verse reference (book, chapter, verse, end_chapter, end_verse)
    and formats verse reference as a string.
    e.g. ('John', 3, 16,) --> 'John 3:16'
    ('2 Cor.', 3, 16, 3, 18) --> '2 Cor. 3:16-18'
    '''
    if ref['chapter'] is not None:
        ref_string = ref['book'] + ' ' + str(ref['chapter']) + ':' + str(ref['verse'])
        if ref['end_chapter'] is not None:
            ref_string += '-'
            if ref['end_chapter'] == ref['chapter']:
                ref_string += str(ref['end_verse'])
            else:
                ref_string += str(ref['end_chapter']) + ':' + str(ref['end_verse'])
        return ref_string
    else:
        return ''

def normalize_reference(bookname=None, chapter=None, verse=None,
                                  end_chapter=None, end_verse=None):
    """
    Get a complete scripture reference with full book name
    from partial data.
    Reference is returned as a dictionary with keys:
    -book (book abbreviation)
    -chapter
    -verse
    -end_chapter
    -end_verse
    """
    book = get_book(bookname)

    # SPECIAL CASE FOR BOOKS WITH ONE CHAPTER:
    # If there is only one chapter in this book, set the chapter to one and
    # treat the incoming chapter argument as though it were the verse.
    # This normalizes references such as:
    # Jude 2 and Jude 2-4
    if len(book[3]) == 1:
        if verse is None and end_chapter is None:
            verse=chapter
            chapter=1
    else:
        # This is not a single chapter book.
        # If a start verse was NOT provided, but an end_verse was- we have a
        # reference such as John 3-4 which is invalid.
        if verse is None and end_verse:
            raise InvalidReferenceException()

    # Convert to integers or leave as None
    chapter = int(chapter) if chapter else None
    verse = int(verse) if verse else None
    end_verse = int(end_verse) if end_verse else None
    if end_verse is not None:
        end_chapter = int(end_chapter) if end_chapter else chapter

    if (chapter < 1 or chapter > len(book[3])) \
    or (verse is not None and (verse < 1 or verse > book[3][chapter-1])) \
    or (end_chapter is not None and (
        end_chapter < 1
        or end_chapter < chapter
        or end_chapter > len(book[3]))) \
    or (end_verse is not None and(
        end_verse < 1
        or (end_chapter and end_verse > book[3][end_chapter-1])
        or (chapter == end_chapter and end_verse < verse))):
        raise InvalidReferenceException()

    return {'book': book[1], 
            'chapter': chapter,
            'verse': verse,
            'end_chapter': end_chapter,
            'end_verse': end_verse}

def get_verses(ref):
    ''' 
    Returns a dictionary {reference: verse} of a verse (or multiple consecutive verses) 
    from a verse reference, represented as a dictionary.
    '''
    book_abbrev = ref['book'].strip('.').replace(' ', '')
    try: 
        if ref['end_chapter'] is None:
            response = urllib2.urlopen("http://rcvapi.herokuapp.com/v/%s/%d/%d" % (book_abbrev, ref['chapter'], ref['verse'],))
        else:
            response = urllib2.urlopen("http://rcvapi.herokuapp.com/vv/%s/%d/%d/%s/%d/%d" % (book_abbrev, ref['chapter'], ref['verse'], book_abbrev, ref['end_chapter'], ref['end_verse'],) )
        data = json.loads('[%s]' % response.read())
        verses = data[0]['verses']
        return verses
    except:
        return {}

# adapted from python-scriptures

import re

from bible_re import testaments, book_re, scripture_re
from models import OutlinePoint, Reference

class InvalidReferenceException(Exception):
    """
    Invalid Reference Exception
    """
    pass

def get_book(name):
    """
    Get a book from its name or None if not found
    """
    for books in testaments.itervalues():
        for book in books:
            if re.match(book[2], name, re.IGNORECASE):
                return book
    return None

def extract(text):
    """
    Extract from a block of text a list of 2-tuples
    containing an outline point and a list of normalized, tupled verse references under that outline point.
    """
    outline = []
    point = OutlinePoint(level=0, string='Scripture Reading:')
    point.save()
    outline.append((point, [],))
    for r in re.finditer(scripture_re, text):
        try:
            # find Roman numerals / outline points
            is_bullet = False
            for i in range(1,5): 
                if r.group(i):
                    point = OutlinePoint(level=i, string=r.group(i))
                    point.save()
                    outline.append((point, [],))
                    is_bullet = True


            if is_bullet == False:
                ref = Reference(outline_point=point)
                outline[-1][1].append(ref)
                if r.group('book'): # reference contains book name
                    ref.book = get_book(r.group('book'))[1]
                    ref.chapter = int(r.group('chapter')) if r.group('chapter') else None
                    ref.verse = int(r.group('verse')) if r.group('verse') else None
                    ref.end_chapter = int(r.group('end_chapter')) if r.group('end_chapter') else None
                    ref.end_verse = int(r.group('end_verse')) if r.group('end_verse') else None
                    if ((ref.end_verse is not None) and (ref.end_chapter is None)):
                        ref.end_chapter = ref.chapter
                    ref.save()
                    if r.group('more_verses'):
                        extract_more_verses(r.group('more_verses'), ref, point, outline)
                        

                else: # get book from previous reference
                    if len(outline[-1][1]) > 1:
                        ref.book = outline[-1][1][-2].book
                    else: # if this is the first reference under an outline point
                        ref.book = outline[-2][1][-1].book
                    if r.group('headless_chapter'): # reference has no book
                        ref.chapter = int(r.group('headless_chapter'))
                        ref.verse = int(r.group('headless_verse')) if r.group('headless_verse') else None
                        ref.end_chapter = int(r.group('headless_end_chapter')) if r.group('headless_end_chapter') else None
                        ref.end_verse = int(r.group('headless_end_verse')) if r.group('headless_end_verse') else None
                        if ((ref.end_verse is not None) and (ref.end_chapter is None)):
                            ref.end_chapter = ref.chapter
                        ref.save()
                        if r.group('more_headless_verses'):
                            extract_more_verses(r.group('more_headless_verses'), ref, point, outline)
                            
                    else:
                        if r.group('lonely_verse'):
                            if len(outline[-1][1]) > 1:
                                ref.chapter = outline[-1][1][-2].chapter
                            else: # this is the first reference under an outline point
                                ref.chapter = outline[-2][1][-1].chapter
                            ref.verse = int(r.group('lonely_verse'))
                            ref.end_verse = int(r.group('lonely_end_verse')) if r.group('lonely_end_verse') else None
                            if ((ref.end_verse is not None) and (ref.end_chapter is None)):
                                ref.end_chapter = ref.chapter
                            ref.save()
                            if r.group('more_lonely_verses'):
                                extract_more_verses(r.group('more_lonely_verses'), ref, point, outline)
                                
        except InvalidReferenceException:
            pass
    return outline


def extract_more_verses(text, ref, point, outline):
    """
    -text: string of verse numbers without book or chapter, e.g. '3, 7, 10-14, 16'.
    -ref: Reference immediately preceding this string of verse numbers.
    -point: outline point the verses are under.
    -outline: outline list from extract().
    Helper function for extract() -- creates References for verses and adds them to outline.
    Creates References for verses and adds them to outline.
    """
    # gets list of tuples: (verse, end_verse,)
    # e.g. '3, 7, 10-14, 16' --> [(3, None,), (7, None,), (10, 14,), (16, None,)]
    verses = re.findall(re.compile(r'(?P<verse>\d{1,3})(?:-(?P<end_verse>\d{1,3}))?'), text)
    
    for verse in verses:
        more_verses_ref = Reference(outline_point=point,
            book=ref.book,
            verse=int(verse[0]))
        more_verses_ref.end_verse = int(verse[1]) if verse[1] else None
        if ref.end_chapter is not None:
            more_verses_ref.chapter = ref.end_chapter
        else:
            more_verses_ref.chapter = ref.chapter
        if more_verses_ref.end_verse is not None:
            more_verses_ref.end_chapter = more_verses_ref.chapter
        more_verses_ref.save()
        outline[-1][1].append(more_verses_ref)

    return

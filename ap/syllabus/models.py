from django.db import models
from classes.models import Class
from books.models import Book

from time import strftime

from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager

from django.core.urlresolvers import reverse, reverse_lazy

""" SYLLABUS models.py

This module catalogs all pertinent data associated with classes in the FTTA
for use in in other functions. For example, Data includes class name, date,
assignments, books, midterms, etc. Inputted data is organized into a
readable form for the entire term.

Data Models:
    - Syllabus:
        classSyllabus (ForeignKey: Class)
    - Session:
        date
        topic
        book (ForeignKey: Book) - name(?), code
        assignment[]
        note
        exam (boolean, HIDDEN)
        syllabus (ForeignKey: Syllabus)
"""

class Syllabus (models.Model):

    # which class this syllabus belongs to
    classSyllabus = models.ForeignKey(Class)

    # whether assignment is read before or after class (== true)
    after = models.BooleanField(default=False)

    # def get_absolute_url(self):
    #     return reverse('self.classSyllabus.code')

    def get_absolute_url(self):
        return '%s/' % self.classSyllabus.term.code #reverse_lazy('detail-view', kwargs={'after': self.classSyllabus.code}) 

    def get_url(self):
        return '%s/' % self.classSyllabus.code

    def get_id(self):
        slug = self.id
        return slug

    # @property
    # def _get_code(self):
    #     code= self.classSyllabus.code
    #     return code
    
    # codes = property(_get_code)

    def __unicode__(self):
        return (self.classSyllabus.name + " | " + self.classSyllabus.term.name)

    # code = Syllabus.classSyllabus.code

    # def get_code(self):
    #     code = self.classSyllabus.term.name
    #     return code


class Session(models.Model):

    # date of the class
    date = models.DateField(verbose_name='session date')

    # topic; "exam";
    topic = models.CharField(max_length=200)

    # book name, code
    """ TO DO: Make this OPTIONAL. """
    """and make this multiple"""
    book = models.ForeignKey(Book) #, blank=True, null=True)

    # assignment info (pages; chapters; msgs; lessons; verses; exam: "FINAL, MIDTERM, ETC")
        # can list multiple assigments, e.g. memory verses
    """this works now, comma is its delimeter"""
    assignment = ArrayField(dbtype="varchar(255)")

    # exam (HIDDEN)
    exam = models.BooleanField(default=False)

    # the class syllabus this session refers to
    syllabus = models.ForeignKey(Syllabus)

    def __unicode__(self):
        return (self.syllabus.classSyllabus.name + " | "
                + self.syllabus.classSyllabus.term.name + " | " + 
                self.date.strftime('%Y/%m/%d') + " | " + self.topic)

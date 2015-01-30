import datetime
import logging
from exceptions import ValueError

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


""" TERM models.py

This schedules module is for representing weekly trainee schedules.

Data Models
- Term:
    a term of the full-time training, consisting of twenty weeks

"""


class Term(models.Model):

    # whether this is the current term
    current = models.BooleanField(default=False)

    # a term's season; i.e. Spring/Fall
    season = models.CharField(max_length=6,
                              choices=(
                                  ('Spring', 'Spring'),
                                  ('Fall', 'Fall'),
                              ),
                              default=None)

    # which year this term is in; e.g. 2014
    year = models.PositiveSmallIntegerField()

    # first day of the term, the monday of pre-training
    start = models.DateField(verbose_name='start date')

    # the last day of the term, the sat of semiannual
    end = models.DateField(verbose_name='end date')

    def _name(self):
        # return term's full name; e.g. Fall 2014
        return self.season + " " + str(self.year)

    name = property(_name)

    def _code(self):
        # return term's short code; e.g. Fa14
        return self.season[:2] + str(self.year)[2:]

    code = property(_code)

    def _length(self):
        """ number of weeks in the term """
        return 20  # hardcoded until it ever changes

    length = property(_length)

    @staticmethod
    def current_term():
        """ Return the current term """
        try:
            return Term.objects.get(current=True)
        except ObjectDoesNotExist:
            logging.critical('Could not find any terms marked as the current term!')
            # try to return term by date (will not work for interim)
            return Term.objects.get(Q(start__lte=datetime.date.today()), Q(end__gte=datetime.date.today()))
        except MultipleObjectsReturned:
            logging.critical('More than one term marked as current term! Check your Term models')
            # try to return term by date (will not work for interim)
            return Term.objects.get(Q(start__lte=datetime.date.today()), Q(end__gte=datetime.date.today()))

    @staticmethod
    def set_current_term(term):
        """ Set term to current, set all other terms to not current """
        Term.objects.filter(current=True).update(current=False)
        term.current = True


    def get_date(self, week, day):
        """ return an absolute date for a term week/day pair """
        return self.start + datetime.timedelta(week * 7 + day)

    def reverse_date(self, date):
        """ returns a term week/day pair for an absolute date, starting from 0/0 """
        if self.start <= date <= self.end:
            # days since the term started
            delta = date - self.start
            return (delta.days / 7, delta.days % 7)
        # if not within the dates the term, raise an error
        else:
            raise ValueError('Invalid date for this term: ' + str(date))

    def get_absolute_url(self):
        return reverse('terms:detail', kwargs={'code': self.code})

    def __unicode__(self):
        return self.name

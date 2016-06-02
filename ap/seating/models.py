from django.db import models

from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager

from terms.models import Term
from accounts.models import Trainee

""" seating/models.py

Chart: contains seats and trainees

Seat: intermediate model between Charts and Trainees M2M relationship

Partial: a subsection of a Chart
"""


class Chart(models.Model):
    """ Defines a seating chart, with trainees associated to seats"""

    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255, null=True, blank=True)

    term = models.ForeignKey(Term)

    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()

    trainees = models.ManyToManyField(Trainee, through='Seat')

    def __unicode__(self):
        return self.term.__unicode__() + ' ' + self.name


class Seat(models.Model):
    """ Intermediate model to relate a Trainee to a seating Chart """
    trainee = models.ForeignKey(Trainee)
    chart = models.ForeignKey(Chart)

    # coordinates
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()

    def __unicode__(self):
        return "%s on %s @ (%s, %s)" % {self.trainee, self.chart, self.x, self.y }


class Partial(models.Model):
    """ Defines a subset of a seating chart. Mainly used for entering roll """

    chart = models.ForeignKey(Chart)

    # upper and lower bounds on x and y axis
    x_lower = models.SmallIntegerField()
    x_upper = models.SmallIntegerField()
    y_lower = models.SmallIntegerField()
    y_upper = models.SmallIntegerField()

    def __unicode__(self):
        return "%s from (%s, %s) to (%s, %s)" % {self.chart, self.x_lower, self.y_lower, self.x_upper, self.y_upper}

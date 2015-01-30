import datetime

from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import Trainee
from attendance.utils import Period
from books.models import Book
from schedules.models import Schedule
from terms.models import Term


""" lifestudies models.py
This discipline module handles the assigning and managing of
the life-study summaries from the TA side and the submitting
from the trainees' side.

DISCIPLINE
    - A discipline is assigned by TA to a single trainees, along with the
      number of summaries needed to complete it.
    - The model methods are mostly invovled with the summaries that are
      related to it.
    - A discipline is completed when ALL summaries associated are approved
    - approving a discipline is done by approving all related summaries

SUMMARY
    - A summary is related to a single book and has the content inputted by
      a trainee.

"""


class Discipline(models.Model):

    TYPE_OFFENSE_CHOICES = (
        ('MO', 'Monday Offense'),
        ('RO', 'Regular Offense'),
    )

    TYPE_INFRACTION_CHOICES = (
        ('AT', 'Attendance'),
        ('CI', 'Cell Phone & Internet'),
        ('MS', 'Missed Service'),
        ('S', 'Speeding'),
        ('AN', 'Alarm Noise'),
        ('G', 'Guard'),
        ('C', 'Curfew'),
        ('M', 'Misplaced Item'),
        ('HI', 'House Inspection'),
        ('L', 'Library'),
        ('MISC', 'Misc'),
    )

    # an infraction is the reason for the trainee to be assigned discipline
    infraction = models.CharField(choices=TYPE_INFRACTION_CHOICES,
                                  max_length=4)

    # a quantity refers to how many summaries are assigned
    quantity = models.PositiveSmallIntegerField()

    # the date of the assignment of the discipline.
    date_assigned = models.DateTimeField(auto_now_add=True)

    # the due date and time for the discipline to be submitted by
    due = models.DateField()

    # the type of offense being assigned
    offense = models.CharField(choices=TYPE_OFFENSE_CHOICES, default='RO',
                               max_length=2)

    trainee = models.ForeignKey(Trainee)

    #sort disciplines by name
    class Meta:
        ordering = ["trainee__account__firstname"]

    def approve_all_summary(self):
        for summary in self.summary_set.all():
            summary.approve()
        self.save()
        return self.summary_set.all()

    def get_num_summary_due(self):
        """get the number of summary that still needs to be submitted"""
        return self.quantity - len(self.summary_set.all())

    def get_num_summary_approved(self):
        """get the number of summary that still needs to be approved"""
        num = 0
        for summary in self.summary_set.all():
            if summary.approved is True:
                num = num + 1
        return num

    #if this is True it means all the lifestudies has been approved and all
    #have been submitted. This assume num of summary submitted not larger
    #than num of summary assigned
    def is_completed(self):
        if self.get_num_summary_due() > 0:
            return False
        else:
            for summary in self.summary_set.all():
                if summary.approved is False:
                    return False
        return True

    @staticmethod
    def calculate_summary(trainee, period):
        """this function examines the Schedule belonging to trainee and search
        through all the Events and Rolls. Returns the number of summary a
        trainee needs to be assigned over the given period."""
        num_A = 0
        num_T = 0
        num_summary = 0
        for roll in trainee.rolls.all():
            if roll.event.date >= Period().start(period) and roll.event.date <= Period().end(period):
                if roll.status == 'A':
                    num_A += 1
                elif roll.status == 'L' or roll.status == 'T' or \
                        roll.status == 'U':
                    num_T += 1
        if num_A >= 2:
            num_summary += num_A
        if num_T >= 5:
            num_summary += num_T - 3
        return num_summary

    def __unicode__(self):
        return "[{offense}] {name}. Infraction: {infraction}. Quantity: \
            {quantity}. Still need {num_summary_due} summaries. Completed: \
            {is_completed}".format(
            name=self.trainee.account.get_full_name(),
            infraction=self.infraction, offense=self.offense,
            quantity=self.quantity, num_summary_due=self.get_num_summary_due(),
            is_completed=self.is_completed())


class Summary(models.Model):
    # the content of the summary (> 250 words)
    content = models.TextField()

    # the book assigned to summary
    # relationship: many summaries to one book
    book = models.ForeignKey(Book)

    # the chapter assigned to summary
    chapter = models.PositiveSmallIntegerField()

    # if the summary has been approved
    approved = models.BooleanField(default=False)

    # which discipline this summary is associated with
    discipline = models.ForeignKey(Discipline)

    # automatically generated date when summary is submitted
    date_submitted = models.DateTimeField(auto_now_add=True)

    #sort summaries by name
    class Meta:
        ordering = ["approved"]

    def __unicode__(self):
        return "[{book} ch. {chapter}] {name}. Approved: {approved}".format(
            name=self.discipline.trainee.account.get_full_name,
            book=self.book.name, chapter=self.chapter, approved=self.approved)

    def approve(self):
        self.approved = True
        self.save()
        return self

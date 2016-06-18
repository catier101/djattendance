from datetime import date

from schedules.constants import WEEKDAYS
from django.db import models
from schedules.models import Event
from accounts.models import Trainee
from terms.models import Term

""" attendance models.py
The attendance module takes care of data and logic directly related
to tracking attendance. It does not handle things such as schedules
or leave slips.

DATA MODELS:
    - Roll: an attendance record per trainee, per event.
            for example, if 10 trainees are supposed to be at an event,
            then there will be 10 roll objects associated to that event,
            as well as each trainee.
"""


class Roll(models.Model):

    ROLL_STATUS = (
        ('A', 'Absent'),
        ('T', 'Tardy'),
        ('U', 'Uniform'),
        ('L', 'Left Class'),
        ('P', 'Present')
    )

    event = models.ForeignKey(Event)

    trainee = models.ForeignKey(Trainee, related_name='rolls')

    status = models.CharField(max_length=5, choices=ROLL_STATUS, default='P')

    # once a roll is finalized, it can no longer be edited
    # except by a TA, attendance monitor, or other admin
    finalized = models.BooleanField(default=False)

    notes = models.CharField(max_length=200, blank=True)

    # the one who submitted this roll
    # for first year should be an attendance monitor, house coordinator, team monitor, or YPC monitor
    # for second year it can either by a second year trainee and/or any of the roles listed above
    # for second year there can be two roll objects per event, one submitted by the second year trainee and one submitted by a monitor, this is for audits

    submitted_by = models.ForeignKey(Trainee, null=True, related_name='submitted_rolls')

    # when the roll was last updated
    last_modified = models.DateTimeField(auto_now=True)

    # the date of the event that corresponds with the roll.
    date = models.DateField()

    def __unicode__(self):
        # return status, trainee name, and event
        return "[%s] %s @ %s" % (self.status, self.trainee, self.event)

    @staticmethod
    def update_or_create(validated_data):
        '''
            Creates roll if not existing, else update
            Reteurn None if event doesn't exist for roll
        '''
        
        event = validated_data['event']
        date = validated_data['date']
        submitted_by = validated_data['submitted_by']
        
        # checks if event exists for given event and date
        event_override = Event.objects.filter(name=event.name, weekday=date.weekday())

        if not event_override:
            return None

        newroll, created = Roll.objects.update_or_create(**validated_data)

        return newroll

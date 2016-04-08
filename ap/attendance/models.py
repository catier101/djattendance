from datetime import date

from django.db import models
from schedules.models import Event
from accounts.models import Trainee
from terms.models import Term

from django.contrib.auth.models import Group

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

    class Meta:
        permissions = (
            ("attendance_all", "Can view roll"),
            )

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
    monitor = models.ForeignKey(Trainee, null=True, related_name='submitted_rolls')

    # when the roll was last updated
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        # return status, trainee name, and event
        return "[%s] %s @ %s" % (self.status, self.trainee, self.event)

    # 
    # TA_group.permissions.add

    # TA_group.permission.add()

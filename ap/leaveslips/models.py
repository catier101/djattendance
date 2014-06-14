from django import forms
from django.db import models
from django.core.urlresolvers import reverse

from datetime import datetime, timedelta

from schedules.models import Event
from accounts.models import Trainee, TrainingAssistant


""" leaveslips models.py
The leavelslip module takes care of all logic related to... you guessed it, leave slips.


DATA MODELS:
    - LeaveSlip: an abstract class that contains information common to all leave
    leave slips. Extended by Individual and Group slips.

    - IndividualSlip: extends LeaveSlip generic class. A leave slip that only
    applies to one trainee (but can apply to multiple events)

    - GroupSlip: extends LeaveSlip generic class. A leaveslip that can apply to
    a group of trainees, and covers a time range (rather than certain events).

    - MealOutSlip: an extension to a leaveslip, containing information relevant
    to a pre-excused meal out.

    - NightOutSlip: an extension to a leaveslip, containing information relevant
    to a pre-excused night out.
"""


class LeaveSlip(models.Model):

    LS_TYPES = (
        ('CONF', 'Conference'),
        ('EMERG', 'Family Emergency'),
        ('FWSHP', 'Fellowship'),
        ('FUNRL', 'Funeral'),
        ('GOSP', 'Gospel'),
        ('INTVW', 'Grad School/Job Interview'),
        ('GRAD', 'Graduation'),
        ('MEAL', 'Meal Out'),
        ('NIGHT', 'Night Out'),
        ('OTHER', 'Other'),
        ('SERV', 'Service'),
        ('SICK', 'Sickness'),
        ('SPECL', 'Special'),
        ('WED', 'Wedding'),
        ('NOTIF', 'Notification Only'),
    )

    LS_STATUS = (
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('F', 'Fellowship'),
        ('D', 'Denied'),
        ('S', 'TA sister approved'),
    )

    type = models.CharField(max_length=5, choices=LS_TYPES)
    status = models.CharField(max_length=1, choices=LS_STATUS, default='P')

    TA = models.ForeignKey(TrainingAssistant)
    trainee = models.ForeignKey(Trainee)#trainee who submitted the leaveslip

    submitted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    finalized = models.DateTimeField(blank=True, null=True)  # when this leave-slip was approved/denied

    description = models.TextField(blank=True, null=True)  # trainee-supplied
    comments = models.TextField(blank=True, null=True)  # for TA comments

    texted = models.BooleanField(default=False)  # for sisters only

    informed = models.BooleanField(blank=True, default=False)  # not sure, need to ask

    def __init__(self, *args, **kwargs):
        super(LeaveSlip, self).__init__(*args, **kwargs)
        self.old_status = self.status

    def save(self, force_insert=False, force_update=False):
        #records the datetime when leaveslip is either approved or denied
        if (self.status == 'D' or self.status == 'A') and (self.old_status == 'P' or self.old_status == 'F' or self.old_status == 'S'):
            self.finalized = datetime.now()
        super(LeaveSlip, self).save(force_insert, force_update)
        self.old_status = self.status

    class Meta:
        abstract = True


class IndividualSlip(LeaveSlip):

    events = models.ManyToManyField(Event)

    def get_update_url(self):
        return reverse('leaveslips:individual-update', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('leaveslips:individual-detail', kwargs={'pk': self.id})

    def _late(self):
        end_date = self.events.all().order_by('-end')[0].end
        if self.submitted > end_date+timedelta(days=2):
            return True
        else:
            return False

    late = property(_late)  # whether this leave slip was submitted late or not


class GroupSlip(LeaveSlip):

    start = models.DateTimeField()
    end = models.DateTimeField()
    trainee_group = models.ManyToManyField(Trainee, related_name='group') #trainees included in the leaveslip

    def get_update_url(self):
        return reverse('leaveslips:group-update', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('leaveslips:group-detail', kwargs={'pk': self.id})

class MealOutSlip(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    leaveslip = models.OneToOneField(IndividualSlip)

class NightOutSlip(models.Model):

    hostname = models.CharField(max_length=255)
    phone = models.PositiveIntegerField()
    hostaddress = models.CharField(max_length=255)
    HC = models.ForeignKey(Trainee)
    leaveslip = models.OneToOneField(IndividualSlip)

# form classes
class IndividualSlipForm(forms.ModelForm):
    class Meta:
        model = IndividualSlip
        fields = ['type', 'description', 'comments', 'texted', 'informed', 'events']

class GroupSlipForm(forms.ModelForm):
    class Meta:
        model = GroupSlip
        fields = ['type', 'trainee_group', 'description', 'comments', 'texted', 'informed', 'start', 'end']

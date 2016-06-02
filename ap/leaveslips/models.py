from django import forms
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from attendance.models import Roll
from accounts.models import Trainee, TrainingAssistant
from django.db.models.signals import pre_delete
from django.dispatch import receiver


""" leaveslips models.py
The leavelslip module takes care of all logic related to... you guessed it, leave slips.


DATA MODELS:
    - LeaveSlip: an abstract class that contains information common to all leave
    leave slips. Extended by Individual and Group slips.

    - IndividualSlip: extends LeaveSlip generic class. A leave slip that only
    applies to one trainee (but can apply to multiple events)

    - GroupSlip: extends LeaveSlip generic class. A leaveslip that can apply to
    a group of trainees, and covers a time range (rather than certain events).
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

    TA = models.ForeignKey(TrainingAssistant, blank=True, null=True)
    trainee = models.ForeignKey(Trainee, related_name='%(class)ss')  #trainee who submitted the leaveslip

    submitted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    finalized = models.DateTimeField(blank=True, null=True)  # when this leave-slip was approved/denied

    description = models.TextField(blank=True, null=True)  # trainee-supplied
    comments = models.TextField(blank=True, null=True)  # for TA comments

    texted = models.BooleanField(default=False)  # for sisters only

    informed = models.BooleanField(blank=True, default=False)  # not sure, need to ask

    @property
    def classname(self):
        # returns whether slip is individual or group
        return str(self.__class__.__name__)[:-4].lower()

    def __init__(self, *args, **kwargs):
        super(LeaveSlip, self).__init__(*args, **kwargs)
        self.old_status = self.status

    def create(self, force_insert=False, force_update=False):
        #records the datetime when leaveslip is either approved or denied
        #save the old status and compare with current status and record finalized datetime only if transitioning
        #out of a regular state to a deny or approved. This safeguards against duplicate approval or denial.
        if (self.status == 'D' or self.status == 'A') and (self.old_status == 'P' or self.old_status == 'F' or self.old_status == 'S'):
            self.finalized = datetime.now()
        super(LeaveSlip, self).save(force_insert, force_update)
        self.old_status = self.status

    # deletes dummy roll under leave slip.


    def delete_dummy_rolls(self, roll):
        if Roll.objects.filter(leaveslips__id=self.id, id=roll.id).exist() and roll.status == 'P':
            Roll.objects.filter(id=roll.id).delete() 

    @property
    def events(self):
        evs = []
        for roll in self.rolls.all():
            roll.event.date = roll.date
            evs.append(roll.event)
        return evs

    def __unicode__(self):
        return "[%s] %s - %s" % (self.submitted.strftime('%m/%d'), self.type, self.trainee)

    class Meta:
        abstract = True

class IndividualSlip(LeaveSlip):

    rolls = models.ManyToManyField(Roll, related_name='leaveslips')

    @receiver(pre_delete)
    def delete_individualslip(sender, instance, **kwargs):
        if isinstance(instance, IndividualSlip):
            for roll in instance.rolls.all():
                if roll.status == 'P':
                    Roll.objects.filter(id=roll.id).delete()

    def get_update_url(self):
        return reverse('leaveslips:individual-update', kwargs={'pk': self.id})

    @property
    def late(self):
        roll = self.rolls.order_by('-date')[0]
        date = roll.date
        time = roll.event.end
        if self.submitted > datetime(date,time) + timedelta(hours=48):
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('leaveslips:individual-detail', kwargs={'pk': self.id})

class GroupSlip(LeaveSlip):

    start = models.DateTimeField()
    end = models.DateTimeField()
    trainees = models.ManyToManyField(Trainee, related_name='group')  #trainees included in the leaveslip

    def get_update_url(self):
        return reverse('leaveslips:group-update', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('leaveslips:group-detail', kwargs={'pk': self.id})

    def _events(self):
        """ equivalent to IndividualSlip.events """
        return Event.objects.filter(start__gte=self.start).filter(end__lte=self.end)

    events = property(_events)
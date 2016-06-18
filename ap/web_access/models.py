from django.db import models
from django.core.urlresolvers import reverse

from accounts.models import Trainee

""" web-access models.py
This module handles requests for Internet access either made by trainees or for
a guest by their MAC address.

REQUEST
    - This model represents a web-access request submitted by a trainee or
    guest.

"""


class WebRequest(models.Model):

    TYPE_APPROVAL_STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('F', 'Marked for Fellowship'),
        ('D', 'Denied'),
        ('E', 'Expired'),
    )

    TYPE_REASON_CHOICES = (
        ('Go', 'Gospel'),
        ('Sr', 'Service'),
        ('GA', 'Graduate Application'),
        ('Fs', 'Fellowship'),
        ('Ot', 'Other'),
    )

    MINUTES_CHIOCES = (
        (15, '15 minutes'),
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '1 hour'),
        (90, '1 hour 30 minutes'),
        (120, '2 hours'),
        (180, '3 hours'),
        (240, '4 hours'),
        (300, '5 hours'),
    )

    # What state this request is in with respect to the TA's approval.
    status = models.CharField(choices=TYPE_APPROVAL_STATUS_CHOICES, max_length=2, default='P')

    # A reason is a category for the motivation behind the request.
    reason = models.CharField(choices=TYPE_REASON_CHOICES, max_length=2)

    # How many minutes will the web access request be good for once it has been started
    minutes = models.PositiveSmallIntegerField(choices=MINUTES_CHIOCES)

    # The date the request was made.
    date_assigned = models.DateTimeField(auto_now_add=True)

    # The date the request was started.
    time_started = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    # The date the request expires
    date_expire = models.DateField()

    # For a guest web access request this is used to identify the request.
    # for non guests this field is set when the web access request is started.
    # hw_address = MACAddressField(blank=True)

    # For non guests this field is who placed the request.
    trainee = models.ForeignKey(Trainee)

    # Field for comments submitted with the request.
    comments = models.TextField()

    # Field for comments submitted by the TA.
    TA_comments = models.TextField(blank=True, null=True)

    # Whether the request is urgent or not
    urgent = models.BooleanField(default=False)

    def get_update_url(self):
        return reverse('web_access:web_access-update', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('web_access:web_access-detail', kwargs={'pk': self.id})

    # Sort by trainee name
    class Meta:
        ordering = ['date_assigned', 'date_expire', 'trainee__firstname']

    def __unicode__(self):
        return '[{reason}] {name}. Duration: {duration}'.format(
            name=self.trainee.full_name,
            reason=self.reason,
            duration=self.minutes
        )

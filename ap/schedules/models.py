from datetime import datetime, date, time, timedelta
from copy import deepcopy

from django.db import models
from django.core.urlresolvers import reverse

from terms.models import Term
from classes.models import Class
from accounts.models import Trainee
from .utils import next_dow
from schedules.constants import WEEKDAYS

""" SCHEDULES models.py
This schedules module is for representing weekly trainee schedules.
Data Models
- Event:
    an event, such as class or study time, that trainees need to attend.
- WeeklyEvents:
- Schedule:
    a collection of events for one trainee. each trainee should have one
    schedule per term.
- ScheduleTemplate:
    a generic collection of events for one week that can be applied to a
    trainee or group of trainees.
"""


'''
Event - Only defines one particular event. i.e. Full Min (Tuesday morning, weekly)
Can never be something like: Thursday/Saturday evening study
'''
class Event(models.Model):

    # different colors assigned to each event type
    EVENT_TYPES = (
        ('C', 'Class'),
        ('S', 'Study'),
        ('R', 'Rest'),
        ('M', 'Meal'),
        ('H', 'House'),
        ('T', 'Team'),
        ('L', 'Church Meeting'),  # C is taken, so L for locality
        ('*', 'Special'),  # S is taken, so * for special
    )

    MONITOR_TYPES = (
        ('AM', 'Attendance Monitor'),
        ('TM', 'Team Monitor'),
        ('HC', 'House Coordinator'),
    )

    CLASS_TYPE = (
        ('MAIN', 'Main'),
        ('1YR', '1st Year'),
        ('2YR', '2nd Year'),
        ('AFTN', 'Afternoon'),
    )

    # name of event, e.g. Full Ministry of Christ, or Lights Out
    name = models.CharField(max_length=30)

    # the event's shortcode, e.g. FMoC or Lights
    code = models.CharField(max_length=10)

    # a description of the event (optional)
    description = models.CharField(max_length=250, blank=True)

    # if this event is a class, relate it
    # classs = models.ForeignKey(Class, blank=True, null=True, verbose_name='class')  # class is a reserved keyword :(

    # the type of event
    type = models.CharField(max_length=1, choices=EVENT_TYPES, default='C')

    # which type of class this is, e.g. Main, 1st year
    class_type = models.CharField(max_length=4, choices=CLASS_TYPE, blank=True, null=True)

    # who takes roll for this event
    monitor = models.CharField(max_length=2, choices=MONITOR_TYPES, blank=True, null=True)

    # # which term this event is active in
    # term = models.ForeignKey(Term)

    start = models.TimeField()

    end = models.TimeField()

    # Optional to catch one-off days, only happen once
    day = models.DateField(blank=True, null=True)

    weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS, verbose_name='Day of the week', null=True, blank=True)

    @property
    def get_schedules(self):
        return self.schedules.all()

    @property
    def get_weekday(self):
        return WEEKDAYS[self.weekday][1]

    # returns the date of the event for the current week, e.g. 04-20-16
    @property
    def current_week_date(self):
        d = datetime.today()
        d = d - timedelta(d.weekday()) + timedelta(self.weekday)
        return d

    # the date of the event for a given week
    def date_for_week(self, week):
        start_date = Term.current_term().start
        event_week = start_date + timedelta(weeks=week-1)
        return event_week + timedelta(days = self.weekday)

    # checks for time conflicts between events. Returns True if conflict exists.
    def check_time_conflict(self, event):
        return (self.end >= event.start) and (event.end >= self.start)

    # gets the week from an absolute date of the current term.
    def week_from_date(self, date):
        return Term.current_term().term_week_of_date(date)

    def get_absolute_url(self):
        return reverse('schedules:event-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('schedules:event-update', kwargs={'pk': self.id})

    def __unicode__(self):
        return "%s" % (self.name)



class ClassManager(models.Manager):

    def get_queryset(self):
        return super(ClassManager, self).get_queryset().filter(type='C')

class Class(Event):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = 'C'
        print 'custom save', self
        super(Class, self).save(*args, **kwargs)

    objects = ClassManager()


#TODO: ServiceEvents?


'''
Schedules stack on top of each other to create a master schedule for each trainee
Base schedules may include rising schedule, meal schedule, class schedule, night schedule
Special schedules may include a specific campus's work schedule (UCLA, USC, OCC, PCC), ITERO, service week, Thanksgiving
(e.g. Campus - CHAP - Chapman University - Orange, Class - General Class, Conference - Memorial Day Meals)
A complete schedule would result from something like 
Rise + meal + class + UCLA work + UCLA study + night = schedule for UCLA trainee for a normal week
Schedules can not be edited, only cloned + deactivated.
All active schedules carry over from term to term -> 4th termres taken off, 
1st termers addee
Deactivation governed by length of trainees attached to schedule
It is done by taking trainees off schedules, this prevents human 
error of accidentally reactivating a schedule with a stale set of 
trainees attached to it
'''
class Schedule(models.Model):

    name = models.CharField(max_length=255)

    # Optional comments to describe schedule
    comments = models.CharField(max_length=250, blank=True)

    # which trainee this schedule belongs to
    trainees = models.ManyToManyField(Trainee, related_name="schedules", blank=True)

    # which events are on this schedule
    events = models.ManyToManyField(Event, blank=True, related_name="schedules")

    # For override calculation with services?, could -1
    priority = models.SmallIntegerField()

    # weeks schedule is active in selected season (e.g. [1,2,3,4,5,6,7,8,9,10])
    # max_length=50 fits exactly 1 to 20 with commas and no spaces
    weeks = models.CommaSeparatedIntegerField(max_length=50)

    # Only active schedule used for term schedule calculation
    # active = models.BooleanField(default=True)

    # None means valid for both spring + fall
    season = models.CharField(max_length=6,
                              choices=(
                                  ('Spring', 'Spring'),
                                  ('Fall', 'Fall'),
                              ),
                              default=None)

    date_created = models.DateTimeField(auto_now=True)

    import_to_next_term = models.BooleanField(default=False, verbose_name='Auto import schedule to the following term')

    # Hides "deleted" schedule but keeps it for the sake of record
    is_deleted = models.BooleanField(default=False)

    # Events in time range
    def events_in_range(self, start, end):
        evts = [];
        for event in self.events.all():
            if event.end >= start and end >= event.start:    
                evts.append(event)
        return evts
    
    # Whether the schedule has the week
    def active_in_week(self, week):
        weeks = [int(x) for x in self.weeks.split(',')]
        return week in weeks

    @property
    def start_date(self):
        weeks = [int(x) for x in self.weeks.split(',')]
        start_week = weeks[0]
        return Term.current_term().start + timedelta(weeks=start_week - 1)
    
    @property
    def end_date(self):
        weeks = [int(x) for x in self.weeks.split(',')]
        end_week = weeks[len(weeks)-1]
        return Term.current_term().start + timedelta(weeks=end_week - 1)

    def todays_events(self):
        today = datetime.combine(date.today(), time(0,0))
        tomorrow = today + timedelta(days=1)
        return self.events.filter(start__gte=today).filter(end__lte=tomorrow).order_by('start')

    # class Meta:
        # a trainee should only have one schedule per term
        # unique_together = (('trainees', 'events'))

    def __unicode__(self):
        return '%s %s schedule' % (self.name, self.season)

    def get_absolute_url(self):
        return reverse('schedules:schedule-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('schedules:schedule-update', kwargs={'pk': self.id})

    @staticmethod
    def current_term_schedules():
        return Schedule.objects.filter(season=Term.current_term().season, is_deleted=False)
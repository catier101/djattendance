from datetime import datetime, date, time, timedelta
from copy import deepcopy

from django.db import models
from django.core.urlresolvers import reverse

from terms.models import Term
from classes.models import Class
from accounts.models import Trainee
from .utils import next_dow


""" SCHEDULES models.py

This schedules module is for representing weekly trainee schedules.

Data Models
- Event:
    an event, such as class or study time, that trainees need to attend.
- EventGroup:

- Schedule:
    a collection of events for one trainee. each trainee should have one
    schedule per term.
- ScheduleTemplate:
    a generic collection of events for one week that can be applied to a
    trainee or group of trainees.

"""


class Event(models.Model):

    EVENT_TYPES = (
        ('C', 'Class'),
        ('S', 'Study'),
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

    # name of event, e.g. Full Ministry of Christ, or Lights Out
    name = models.CharField(max_length=30)

    # the event's shortcode, e.g. FMoC or Lights
    code = models.CharField(max_length=10)

    # a description of the event (optional)
    description = models.CharField(max_length=250, blank=True)

    # a groupID. used to group repeating events
    group = models.ForeignKey('EventGroup', blank=True, null=True, related_name="events")

    # if this event is a class, relate it
    classs = models.ForeignKey(Class, blank=True, null=True, verbose_name='class')  # class is a reserved keyword :(

    # the type of event
    type = models.CharField(max_length=1, choices=EVENT_TYPES)

    # who takes roll for this event
    monitor = models.CharField(max_length=2, choices=MONITOR_TYPES, blank=True, null=True)

    # which term this event is active in
    term = models.ForeignKey(Term)

    start = models.DateTimeField()

    end = models.DateTimeField()

    def date(self):
        return self.start.date()

    def _week(self):
        self.term.reverseDate(self.start.date)[0]
    week = property(_week)

    def _day(self):
        self.term.reverseDate(self.start.date)[1]
    day = property(_day)

    def get_absolute_url(self):
        return reverse('schedules:event-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "[%s] %s" % (self.start.strftime('%m/%d'), self.name)


class EventGroup(models.Model):

    # which days this event repeats, starting with Monday (0) through LD (6)
    # i.e. an event that repeats on Tuesday and Thursday would be (1,3)
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=250, blank=True)
    repeat = models.CommaSeparatedIntegerField(max_length=20)
    duration = models.PositiveSmallIntegerField()  # how many weeks this event repeats

    def create_children(self, e):
        # create repeating child Events

        events = [] # list of events to create

        for day in map(int, self.repeat.split(",")):
            event = deepcopy(e)
            event.pk = None
            event.start = next_dow(event.start, day)
            event.end = next_dow(event.end, day)
            events.append(event)
            for week in range(1, self.duration):
                event_ = deepcopy(event)
                event_.start += timedelta(7*week)
                event_.end += timedelta(7*week)
                events.append(event_)

        Event.objects.bulk_create(events)

    def delete(self, *args, **kwargs):
        # override delete(): ensure all events in eventgroup are also deleted
        Event.objects.filter(eventgroup=self.id).delete()
        super(EventGroup, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('schedules:eventgroup-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name + " group"


class Schedule(models.Model):

    # which trainee this schedule belongs to
    trainee = models.ForeignKey(Trainee, related_name="schedule")

    # which term this schedule applies to
    term = models.ForeignKey(Term)

    # which events are on this schedule
    events = models.ManyToManyField(Event, blank=True)

    def todays_events(self):
        today = datetime.combine(date.today(), time(0,0))
        tomorrow = today + timedelta(days=1)
        return self.events.filter(start__gte=today).filter(end__lte=tomorrow).order_by('start')

    class Meta:
        # a trainee should only have one schedule per term
        unique_together = (('trainee', 'term'))

    def __unicode__(self):
        return '%s %s schedule' % (self.trainee.full_name, self.term.code)

    def get_absolute_url(self):
        return reverse('schedules:schedule-detail', kwargs={'pk': self.pk})


class ScheduleTemplate(models.Model):

    name = models.CharField(max_length=20)

    eventgroup = models.ManyToManyField(EventGroup)  # TODO: consider refactor using postgres arrays

    def apply(self, schedule):
        """ applies a schedule template to a schedule """
        for eventgrp in EventGroup.objects.filter(scheduletemplate=self.id):
            # iterate over each event inside each event group
            for event in Event.objects.filter(eventgroup=eventgrp.id):
                schedule.events.add(event)

    def apply_multiple(self, schedules):
        """ applies a schedule template to a group of schedules """
        for schedule in schedules:
            self.apply(schedule)

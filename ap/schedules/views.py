from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib.admin.widgets import AdminDateWidget  
from django.shortcuts import render  

from bootstrap3_datetime.widgets import DateTimePicker
from rest_framework import viewsets, filters

from accounts.serializers import BasicTraineeSerializer
from .models import Schedule, Event, Trainee
from .forms import EventForm, ScheduleForm
from .serializers import EventSerializer, ScheduleSerializer, EventFilter, ScheduleFilter
from terms.models import Term
from rest_framework_bulk import BulkModelViewSet
from rest_framework.renderers import JSONRenderer
from aputils.utils import trainee_from_user
from dal import autocomplete
from django.db.models import Q

class SchedulePersonal(generic.TemplateView):
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        context = super(SchedulePersonal, self).get_context_data(**kwargs)
        trainee = trainee_from_user(self.request.user)
        context['schedule'] = Schedule.objects.filter(trainees=trainee)
        context['trainees'] = Trainee.objects.all()
        context['trainees_bb'] = listJSONRenderer.render(TraineeSerializer(context['trainees'], many=True).data)
        return context

class ScheduleDetail(generic.DetailView):
    model = Schedule
    # template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

class ScheduleCreate(generic.CreateView):
    model = Schedule
    template_name = 'schedules/schedule_create.html'
    form_class = ScheduleForm
    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        context = super(ScheduleCreate, self).get_context_data(**kwargs)
        trainee = trainee_from_user(self.request.user)
        context['schedule'] = Schedule.objects.filter(trainees=trainee)
        context['trainees_bb'] = listJSONRenderer.render(BasicTraineeSerializer(Trainee.objects.order_by('lastname'), many=True).data)
        return context
    def form_valid(self, form):
        schedule = form.save()
        return super(ScheduleCreate, self).form_valid(form)

class ScheduleList(generic.ListView):
    model = Schedule
    template_name = 'schedules/schedule_list.html'
    context_object_name = 'schedules'
    def get_queryset(self):
        return Schedule.objects.filter(is_deleted=False)
    # def get_context_data(self, **kwargs):
    #     listJSONRenderer = JSONRenderer()
    #     user = self.request.user
    #     trainee = trainee_from_user(user)
    #     ctx = super(EventList, self).get_context_data(**kwargs)
    #     events = Event.objects.filter(schedules = trainee.schedules.all()).distinct().order_by('name')
    #     ctx['events_with_day'] = events.filter(weekday__isnull=True)
    #     ctx['events_with_weekday'] = events.exclude(weekday__isnull=True)
    #     return ctx

class ScheduleUpdate(generic.UpdateView):
    model = Schedule
    template_name = 'schedules/schedule_update.html'
    form_class = ScheduleForm

class ScheduleDelete(generic.DeleteView):
    model = Schedule
    success_url = '/schedules/schedule/list/'

class ScheduleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Schedule.objects.order_by('name')
        if self.q:
            qs = qs.filter(Q(name__icontains = self.q))
        return qs

class TraineeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Trainee.objects.filter(is_active=True).order_by('lastname')
        if self.q:
            qs = qs.filter(Q(firstname__icontains = self.q) | Q(lastname__icontains = self.q))
        return qs

class EventAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        user = self.request.user
        trainee = trainee_from_user(user)
        qs = Event.objects.filter(schedules = trainee.schedules.all()).distinct().order_by('name')
        if self.q:
            qs = qs.filter(Q(name__icontains = self.q) | Q(code = self.q))
        return qs

class EventCreate(generic.CreateView):
    model = Event
    template_name = 'schedules/event_create.html'
    form_class = EventForm

    def form_valid(self, form):
        event = form.save()
        return super(EventCreate, self).form_valid(form)

class EventDetail(generic.DetailView):
    model = Event
    context_object_name = 'event'

class EventList(generic.ListView):
    model = Event
    template_name = 'schedules/event_list.html'
    context_object_name = 'events'
    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        user = self.request.user
        trainee = trainee_from_user(user)
        ctx = super(EventList, self).get_context_data(**kwargs)
        events = Event.objects.all().order_by('name')
        ctx['events_with_day'] = events.filter(weekday__isnull=True)
        ctx['events_with_weekday'] = events.exclude(weekday__isnull=True)
        return ctx

class EventUpdate(generic.UpdateView):
    model = Event
    template_name = 'schedules/event_update.html'
    form_class = EventForm

class EventDelete(generic.DeleteView):
    model = Event
    success_url = '/schedules/event/list/'


class TermEvents(generic.ListView):
    model = Event
    template_name = 'schedules/term_events.html'
    context_object_name = 'events'

    def get_queryset(self, **kwargs):
        return Event.objects.filter(term=Term.decode(self.kwargs['term']))

    def get_context_data(self, **kwargs):
        context = super(TermEvents, self).get_context_data(**kwargs)
        context['term'] = Term.decode(self.kwargs['term'])
        return context
        
###  API-ONLY VIEWS  ###

class EventViewSet(BulkModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter
    def get_queryset(self):
        user = self.request.user
        trainee = trainee_from_user(user)
        events = Event.objects.filter(schedules = trainee.schedules.all()).distinct()
        return events
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class ScheduleViewSet(BulkModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduleFilter
    def get_queryset(self):
        trainee = trainee_from_user(self.request.user)
        schedule=Schedule.objects.filter(trainees=trainee).distinct()
        return schedule
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllEventViewSet(BulkModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllScheduleViewSet(BulkModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduleFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib.admin.widgets import AdminDateWidget

from bootstrap3_datetime.widgets import DateTimePicker
from rest_framework import viewsets, filters

from .models import Schedule, ScheduleTemplate, Event, EventGroup
from .forms import EventForm, TraineeSelectForm, EventGroupForm
from .serializers import EventSerializer, ScheduleSerializer, EventFilter, ScheduleFilter
from terms.models import Term
from rest_framework_bulk import BulkModelViewSet

from aputils.utils import trainee_from_user


class SchedulePersonal(generic.TemplateView):
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(SchedulePersonal, self).get_context_data(**kwargs)
        trainee = trainee_from_user(self.request.user)
        context['schedule'] = Schedule.objects.filter(trainee=trainee).get(term=Term.current_term())
        return context


class ScheduleDetail(generic.DetailView):
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

    def get_queryset(self):
        trainee = trainee_from_user(self.request.user)
        return Schedule.objects.filter(trainee=trainee).filter(term=Term.current_term())


class EventGroupCreate(generic.FormView):
    template_name = 'schedules/eventgroup_create.html'
    form_class = EventGroupForm

    def get_context_data(self, **kwargs):
        context = super(EventGroupCreate, self).get_context_data(**kwargs)
        context['trainee_select_form'] = TraineeSelectForm()
        return context

    def form_valid(self, form):

        # create the EventGroup
        eg = EventGroup(
            name = form.cleaned_data['name'],
            code = form.cleaned_data['code'],
            description = form.cleaned_data['description'],
            repeat = ",".join(form.cleaned_data['repeat']), 
            duration = form.cleaned_data['duration'])
        eg.save()
        self.success_url = eg.get_absolute_url()  # redirect to created obj

        # create the first event as a template
        e = Event(
            name = form.cleaned_data['name'],
            code = form.cleaned_data['code'],
            description = form.cleaned_data['description'],
            classs = form.cleaned_data['classs'],
            type = form.cleaned_data['type'],
            monitor = form.cleaned_data['monitor'],
            term = form.cleaned_data['term'],
            start = form.cleaned_data['start'],
            end = form.cleaned_data['end'],
            group = eg,)

        eg.create_children(e)  # model method handles event repeating

        # add trainees to events
        for trainee in form.cleaned_data['trainees']:
            if Schedule.objects.filter(trainee=trainee).filter(term=e.term):
                schedule = Schedule.objects.filter(trainee=trainee).filter(term=e.term)[0]
            else: # if trainee doesn't already have a schedule, create it
                schedule = Schedule(trainee=trainee, term=e.term)
                schedule.save()

            schedule.events.add(*eg.events.all())

        return super(EventGroupCreate, self).form_valid(form)


class EventGroupDetail(generic.DetailView):
    model = EventGroup
    context_object_name = "eventgroup"


class EventCreate(generic.CreateView):
    template_name = 'schedules/event_create.html'
    form_class = EventForm

    def get_context_data(self, **kwargs):
        context = super(EventCreate, self).get_context_data(**kwargs)
        context['trainee_select_form'] = TraineeSelectForm()
        return context

    def form_valid(self, form):
        event = form.save()
        for trainee in form.cleaned_data['trainees']:
            # add event to trainee's schedule
            if Schedule.objects.filter(trainee=trainee).filter(term=event.term):
                schedule = Schedule.objects.filter(trainee=trainee).filter(term=event.term)[0]
                schedule.events.add(event)
            else: # if trainee doesn't already have a schedule, create it
                schedule = Schedule(trainee=trainee, term=event.term)
                schedule.save()
                schedule.events.add(event)
        return super(EventCreate, self).form_valid(form)


class EventDetail(generic.DetailView):
    model = Event
    context_object_name = "event"


class EventUpdate(generic.UpdateView):
    model = Event
    template_name = 'schedules/event_update.html'
    form_class = EventForm

    def get_initial(self):
        trainees = []
        for schedule in self.object.schedule_set.all():
            trainees.append(schedule.trainee)
        return {'trainees': trainees}

    def form_valid(self, form):
        event = form.save()

        # remove event from schedules of trainees no longer assigned to this event
        for schedule in event.schedule_set.all():
            if schedule.trainee not in form.cleaned_data['trainees']:
                schedule.events.remove(event)

        for trainee in form.cleaned_data['trainees']:
            # make sure event is in each trainee's schedule
            if Schedule.objects.filter(trainee=trainee).filter(term=event.term):
                schedule = Schedule.objects.filter(trainee=trainee).filter(term=event.term)[0]
                if event not in schedule.events.all():
                    schedule.events.add(event)
            else:
                schedule = Schedule(trainee=trainee, term=event.term)
                schedule.save()
                schedule.events.add(event)

        return super(EventUpdate, self).form_valid(form)


class EventDelete(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('schedules:event-create')


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

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter
    def get_queryset(self):
        user = self.request.user
        events = Event.objects.filter(schedule=user.schedule.get())
        return events
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduleFilter
    def get_queryset(self):
        trainee = trainee_from_user(self.request.user)
        schedule=Schedule.objects.filter(trainee=trainee)
        return schedule
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ScheduleFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)
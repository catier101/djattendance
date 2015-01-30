from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib.admin.widgets import AdminDateWidget

from bootstrap3_datetime.widgets import DateTimePicker
from rest_framework import viewsets

from .models import Schedule, ScheduleTemplate, Event, EventGroup
from .forms import EventForm, TraineeSelectForm
from .serializers import EventSerializer, ScheduleSerializer
from terms.models import Term


class SchedulePersonal(generic.TemplateView):
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(SchedulePersonal, self).get_context_data(**kwargs)
        context['schedule'] = Schedule.objects.filter(trainee=self.request.user.trainee).get(term=Term.current_term())
        return context


class ScheduleDetail(generic.DetailView):
    template_name = 'schedules/schedule_detail.html'
    context_object_name = 'schedule'

    def get_queryset(self):
        return Schedule.objects.filter(trainee=self.request.user.trainee).filter(term=Term.current_term())


class EventCreate(generic.CreateView):
    model = Event
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
    success_url = reverse_lazy('event-create')



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

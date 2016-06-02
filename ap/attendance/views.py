import django_filters
from itertools import chain
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.renderers import JSONRenderer
from .models import Roll
from .serializers import RollSerializer, RollFilter, AttendanceSerializer, AttendanceFilter
from schedules.models import Schedule, Event
from leaveslips.models import IndividualSlip, GroupSlip
from terms.models import Term
from accounts.models import Trainee
from leaveslips.models import IndividualSlip
from leaveslips.forms import IndividualSlipForm
from rest_framework_bulk import (
    BulkModelViewSet
)
from rest_framework.renderers import JSONRenderer
from django.core import serializers

from schedules.serializers import AttendanceEventWithDateSerializer
from leaveslips.serializers import IndividualSlipSerializer

from aputils.utils import trainee_from_user

class AttendancePersonal(TemplateView):
    template_name = 'attendance/attendance_react.html'
    context_object_name = 'context'


    def get_context_data(self, **kwargs):   
        listJSONRenderer = JSONRenderer()
        ctx = super(AttendancePersonal, self).get_context_data(**kwargs)
        user = self.request.user
        trainee = trainee_from_user(user)
        ctx['events'] = trainee.events
        serialized_obj = serializers.serialize('json',  ctx['events'] )
        ctx['schedule'] = Schedule.objects.filter(trainees=trainee)
        ctx['events_bb'] = listJSONRenderer.render(AttendanceEventWithDateSerializer(ctx['events'], many=True).data)
        ctx['trainee'] = trainee
        ctx['attendance'] = Roll.objects.filter(trainee=trainee)
        ctx['leaveslipform'] = IndividualSlipForm()
        ctx['individualleaveslips'] = IndividualSlip.objects.filter(trainee=trainee)
        # ctx['leaveslips'] = chain(list(IndividualSlip.objects.filter(trainee=self.request.user.trainee).filter(events__term=Term.current_term())), list(GroupSlip.objects.filter(trainee=self.request.user.trainee).filter(start__gte=Term.current_term().start).filter(end__lte=Term.current_term().end)))

        return ctx

class RollViewSet(BulkModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RollFilter
    def get_queryset(self):
        user = self.request.user
        trainee = trainee_from_user(user)
        roll = trainee.current_rolls
        return roll
    def allow_bulk_destroy(self, qs, filtered):
        return filtered
        
        # failsafe- to only delete if qs is filtered.
        # return not all(x in filtered for x in qs)

class AttendanceViewSet(BulkModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = AttendanceFilter
    def get_queryset(self):
        user = self.request.user
        trainee = trainee_from_user(user)
        return trainee
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllRollViewSet(BulkModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RollFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllAttendanceViewSet(BulkModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = AttendanceFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

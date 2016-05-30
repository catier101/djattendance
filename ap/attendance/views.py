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
from accounts.models import User, Trainee, TrainingAssistant
from leaveslips.models import IndividualSlip
from leaveslips.forms import IndividualSlipForm
from rest_framework_bulk import (
    BulkModelViewSet
)

from accounts.serializers import TraineeSerializer, TrainingAssistantSerializer
from schedules.serializers import EventSerializer
from leaveslips.serializers import IndividualSlipSerializer

from aputils.utils import trainee_from_user

class AttendancePersonal(TemplateView):
    template_name = 'attendance/attendance_react.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        #jsx.transform('static/js/react/attendance/calendar.jsx', 'static/js/react/attendance/calendar.js')

        listJSONRenderer = JSONRenderer()
        l_render = listJSONRenderer.render

        trainee = trainee_from_user(self.request.user)
        c_term = Term.current_term()


        ctx = super(AttendancePersonal, self).get_context_data(**kwargs)
        ctx.events = Event.objects.filter(term=c_term)
        ctx.trainee = trainee
        ctx.trainee_bb = l_render(TraineeSerializer(trainee).data)
        # ctx.tas = TrainingAssistant.objects.all()
        # ctx.tas_bb = l_render(TrainingAssistantSerializer(ctx.tas.data))

        print 'current term', c_term
        ctx.schedule = Schedule.objects.filter(term=c_term).get(trainee=trainee)
        ctx.events_bb = l_render(EventSerializer(ctx.schedule.events.all(), many=True).data)
        ctx.attendance = Roll.objects.filter(trainee=trainee, event__term=c_term)
        ctx.attendance_bb = l_render(RollSerializer(ctx.attendance, many=True).data)
        ctx.leaveslipform = IndividualSlipForm()
        print 'trainee', trainee, IndividualSlip.objects.filter(trainee=trainee), IndividualSlip.objects.filter(trainee=trainee, events__term=c_term)
        ctx.leaveslips = IndividualSlip.objects.filter(trainee=trainee, events__term=c_term)
        ctx.groupslips = GroupSlip.objects.filter(trainee=trainee, start__gte=c_term.start, end__lte=c_term.end)
        print 'slips', ctx.leaveslips
        ctx.leaveslips_bb = l_render(IndividualSlipSerializer(ctx.leaveslips, many=True).data)
        return context

class RollViewSet(BulkModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RollFilter
    def get_queryset(self):
        user = self.request.user
        trainee = trainee_from_user(user)
        roll = Roll.objects.filter(trainee=(trainee), event__term=Term.current_term())
        return roll
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AttendanceViewSet(BulkModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AttendanceFilter
    def get_queryset(self):
        user = self.request.user
        trainee = Trainee.objects.filter(account=user)
        return trainee
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllRollViewSet(BulkModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = RollFilter
    def get_queryset(self):
        queryset = Roll.objects.all()
        data = self.request.get_full_path()
        if ('_' not in data):
            return queryset
        data = data.split('_',1)[1]
        data = data.split('&and_')
        or_params = {}
        and_params = {}
        for key in data:
            if '&or_' in key:
                firstFilter=True
                splitdata = key.split('&or_')
                for splitdata2 in splitdata:
                    or_data = splitdata2.split('=')
                    if (or_data[1]=='True'):
                        or_data[1] = True
                    elif (or_data[1]=='False'):
                        or_data[1] = False
                    or_params[or_data[0]] = or_data[1]
                    if firstFilter:
                        queryset = queryset.filter(**or_params)
                        firstFilter=False
                    else:
                        queryset = queryset | Roll.objects.filter(**or_params)
                    or_params={}
            else:
                splitdata=key.split('=')
                if (splitdata[1]=='True'):
                    splitdata[1] = True
                elif (splitdata[1]=='False'):
                    splitdata[1] = False
                and_params[splitdata[0]] = splitdata[1]
                queryset = queryset.filter(**and_params)
                and_params={}
        return queryset
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllAttendanceViewSet(BulkModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AttendanceFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

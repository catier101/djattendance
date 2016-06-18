import django_filters

from itertools import chain
from datetime import datetime

from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from rest_framework import viewsets, filters

from .models import LeaveSlip, IndividualSlip, GroupSlip
from .forms import IndividualSlipForm, GroupSlipForm
from .serializers import IndividualSlipSerializer, IndividualSlipFilter, GroupSlipSerializer, GroupSlipFilter
from accounts.models import Trainee
from rest_framework_bulk import BulkModelViewSet

from aputils.utils import trainee_from_user

# individual slips
class IndividualSlipCreate(generic.CreateView):
    model = IndividualSlip
    template_name = 'leaveslips/individual_create.html'
    form_class = IndividualSlipForm

    def form_valid(self, form):
        print 'Make home in my heart, Lord!'
        self.object = form.save(commit=False)
        self.object.status = 'P'
        trainee = trainee_from_user(self.request.user)
        self.object.trainee = trainee
        self.object.TA = trainee.TA
        self.object.save()
        return super(generic.CreateView, self).form_valid(form)

class IndividualSlipDetail(generic.DetailView):
    model = IndividualSlip
    template_name = 'leaveslips/individual_detail.html'
    context_object_name = 'leaveslip'

class IndividualSlipUpdate(generic.UpdateView):
    model = IndividualSlip
    template_name = 'leaveslips/individual_update.html'
    form_class = IndividualSlipForm

class IndividualSlipDelete(generic.DeleteView):
    model = IndividualSlip
    success_url='/leaveslips/'    


# group slips
class GroupSlipCreate(generic.CreateView):
    model = GroupSlip
    template_name = 'leaveslips/group_create.html'
    form_class = GroupSlipForm
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status = 'P'
        trainee = trainee_from_user(self.request.user)
        self.object.trainee = trainee
        self.object.TA = trainee.TA
        self.object.save()
        return super(generic.CreateView, self).form_valid(form)


class GroupSlipDetail(generic.DetailView):
    model = GroupSlip
    template_name = 'leaveslips/group_detail.html'
    context_object_name = 'leaveslip'

class GroupSlipUpdate(generic.UpdateView):
    model = GroupSlip
    template_name = 'leaveslips/group_update.html'
    form_class = GroupSlipForm

class GroupSlipDelete(generic.DeleteView):
    model = GroupSlip
    success_url='/leaveslips/'


# viewing the leave slips
class LeaveSlipList(generic.ListView):
    model = IndividualSlip, GroupSlip
    template_name = 'leaveslips/list.html'

    def get_queryset(self):
         individual=IndividualSlip.objects.filter(trainee=self.request.user.id).order_by('status')
         group=GroupSlip.objects.filter(trainee=self.request.user.id).order_by('status')  # if trainee is in a group leaveslip submitted by another user
         queryset= chain(individual,group)  # combines two querysets
         return queryset

class TALeaveSlipList(generic.ListView):
    model = IndividualSlip, GroupSlip
    template_name = 'leaveslips/ta_list.html'
    context_object_name = "leaveslips"

    def get_queryset(self):
         individual=IndividualSlip.objects.filter(status__in=['P', 'F', 'S']).order_by('submitted')
         group=GroupSlip.objects.filter(status__in=['P', 'F', 'S']).order_by('submitted')  # if trainee is in a group leaveslip submitted by another user
         queryset= chain(individual,group)  # combines two querysets
         return queryset

def modify_status(request, classname, status, id):
    if classname == "individual":
        leaveslip = get_object_or_404(IndividualSlip, pk=id)
    if classname == "group":
        leaveslip = get_object_or_404(GroupSlip, pk=id)
    leaveslip.status = status
    leaveslip.save()

    message =  "%s's %s leaveslip was " % (leaveslip.trainee, leaveslip.get_type_display().upper()) 
    if status == 'A':
        message += "approved."
    if status == 'D':
        message += "denied."
    if status == 'F':
        message += "marked for fellowship."
    messages.add_message(request, messages.SUCCESS, message)

    return redirect('leaveslips:ta-leaveslip-list')


""" API Views """

class IndividualSlipViewSet(BulkModelViewSet):
    queryset = IndividualSlip.objects.all()
    serializer_class = IndividualSlipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IndividualSlipFilter
    def get_queryset(self):
        trainee = trainee_from_user(self.request.user)
        individualslip=IndividualSlip.objects.filter(trainee=trainee)
        return individualslip
    def allow_bulk_destroy(self, qs, filtered):
        return filtered

        # failsafe- to only delete if qs is filtered.
        # return not all(x in filtered for x in qs)

class GroupSlipViewSet(BulkModelViewSet):
    queryset = GroupSlip.objects.all()
    serializer_class = GroupSlipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = GroupSlipFilter
    def get_queryset(self):
        trainee = trainee_from_user(self.request.user)
        groupslip=GroupSlip.objects.filter(trainee=trainee)
        return groupslip
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllIndividualSlipViewSet(BulkModelViewSet):
    queryset = IndividualSlip.objects.all()
    serializer_class = IndividualSlipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = IndividualSlipFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)

class AllGroupSlipViewSet(BulkModelViewSet):
    queryset = GroupSlip.objects.all()
    serializer_class = GroupSlipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = GroupSlipFilter
    def allow_bulk_destroy(self, qs, filtered):
        return not all(x in filtered for x in qs)
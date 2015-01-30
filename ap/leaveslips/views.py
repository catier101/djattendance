from itertools import chain
from datetime import datetime

from django.views import generic
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy

from rest_framework import viewsets

from .models import LeaveSlip, IndividualSlip, GroupSlip, IndividualSlipForm, GroupSlipForm
from .serializers import IndividualSlipSerializer, GroupSlipSerializer
from accounts.models import Profile

# individual slips
class IndividualSlipCreate(generic.CreateView):
    model = IndividualSlip
    template_name = 'leaveslips/individual_create.html'
    form_class = IndividualSlipForm

    def form_valid(self, form):
        print 'Make home in my heart, Lord!'
        self.object = form.save(commit=False)
        self.object.status = 'P'
        self.object.trainee = self.request.user.trainee
        self.object.TA = self.request.user.trainee.TA
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
            self.object.trainee = self.request.user.trainee
            self.object.TA = self.request.user.trainee.TA
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
         group=GroupSlip.objects.filter(trainee=self.request.user.id).order_by('status') #if trainee is in a group leaveslip submitted by another user
         queryset= chain(individual,group) #combines two querysets
         return queryset



class IndividualSlipViewSet(viewsets.ModelViewSet):
    queryset = IndividualSlip.objects.all()
    serializer_class = IndividualSlipSerializer


class GroupSlipViewSet(viewsets.ModelViewSet):
    queryset = GroupSlip.objects.all()
    serializer_class = GroupSlipSerializer

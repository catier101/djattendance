from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, UpdateView

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Trainee, TrainingAssistant
from .forms import UserForm, EmailForm
from .serializers import UserSerializer, TraineeSerializer, TrainingAssistantSerializer


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/user_detail.html'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/update_user.html'

    def get_success_url(self):
        messages.success(self.request,
                         "User Information Updated Successfully!")
        return reverse_lazy('user_detail', kwargs={'pk': self.kwargs['pk']})


class EmailUpdateView(UpdateView):
    model = User
    form_class = EmailForm
    template_name = 'accounts/email_change.html'

    def get_success_url(self):
        messages.success(self.request, "Email Updated Successfully!")
        return reverse_lazy('user-detail', kwargs={'pk': self.kwargs['pk']})


""" API Views """

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TraineeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


class TrainingAssistantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrainingAssistant.objects.all()
    serializer_class = TrainingAssistantSerializer


class TraineesByGender(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        gender = self.kwargs['gender']
        return Trainee.objects.filter(account__gender=gender)


class TraineesByTerm(APIView):
    model = Trainee

    def get(self, request, format=None, **kwargs):
        term = int(kwargs['term'])
        trainees = [trainee for trainee in list(Trainee.objects.filter(active=True)) if trainee.current_term==term]
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)


class TraineesByTeam(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        team = self.kwargs['pk']
        return Trainee.objects.filter(team__id=team)


class TraineesByTeamType(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        type = self.kwargs['type'].upper()
        return Trainee.objects.filter(team__type=type)


class TraineesByHouse(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        house = self.kwargs['pk']
        return Trainee.objects.filter(house__id=house)


class TraineesByLocality(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        locality = self.kwargs['pk']
        return Trainee.objects.filter(locality__id=locality)


class TraineesHouseCoordinators(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        return Trainee.objects.filter(account__groups__name__iexact="house coordinators")

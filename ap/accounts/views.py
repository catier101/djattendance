from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import DetailView, UpdateView, ListView, TemplateView

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import User, Trainee, TrainingAssistant
from .forms import UserForm, EmailForm
from .serializers import BasicUserSerializer, UserSerializer, TraineeSerializer, TrainingAssistantSerializer


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/user_detail.html'

class EventsListView(ListView):
    model = Trainee
    context_object_name = 'events'
    template_name = 'accounts/events_list.html'
    def get_queryset(self):
        trainee = self.request.user.trainee
        queryset = trainee.events
        return queryset

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


class SwitchUserView(TemplateView):
    template_name = 'accounts/switch_user.html'

    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        l_render = listJSONRenderer.render

        users = User.objects.filter(is_active=True)

        context = super(SwitchUserView, self).get_context_data(**kwargs)
        context['users'] = users
        context['users_bb'] = l_render(BasicUserSerializer(users, many=True).data)

        return context

    def post(self, request, *args, **kwargs):
        """this manually creates Disciplines for each house member"""
        if request.method == 'POST':
            print request.POST, request.POST['id']

            user = User.objects.get(id=request.POST['id'])

            logout(request)

            # This is a terrible way to do log-in users, figure out how to do in a better way in the future
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            return HttpResponseRedirect(reverse_lazy('home'))


""" API Views """

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TraineeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trainee.objects.filter(is_active=True)
    serializer_class = TraineeSerializer


class TrainingAssistantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrainingAssistant.objects.filter(is_active=True)
    serializer_class = TrainingAssistantSerializer


class TraineesByGender(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        gender = self.kwargs['gender']
        return Trainee.objects.filter(account__gender=gender).filter(is_active=True)


class TraineesByTerm(APIView):
    model = Trainee

    def get(self, request, format=None, **kwargs):
        term = int(kwargs['term'])
        trainees = [trainee for trainee in list(Trainee.objects.filter(is_active=True)) if trainee.current_term==term]
        serializer = TraineeSerializer(trainees, many=True)
        return Response(serializer.data)


class TraineesByTeam(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        team = self.kwargs['pk']
        return Trainee.objects.filter(team__id=team).filter(is_active=True)


class TraineesByTeamType(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        type = self.kwargs['type'].upper()
        return Trainee.objects.filter(team__type=type).filter(is_active=True)


class TraineesByHouse(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        house = self.kwargs['pk']
        return Trainee.objects.filter(house__id=house).filter(is_active=True)


class TraineesByLocality(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        locality = self.kwargs['pk']
        return Trainee.objects.filter(locality__id=locality).filter(is_active=True)


class TraineesHouseCoordinators(generics.ListAPIView):
    serializer_class = TraineeSerializer
    model = Trainee

    def get_queryset(self):
        return Trainee.objects.filter(account__groups__name__iexact="house coordinators").filter(is_active=True)




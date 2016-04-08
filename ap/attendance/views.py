from itertools import chain

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView

from django.contrib.admin import AdminSite

from braces import views
from braces.views import PermissionRequiredMixin

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes

from .models import Roll
from .permissions import AttendanceAllorIsOwner, AttendanceAll
from .admin import admin_site

# TODO: globalize this permission, install docutils for admin. Look up exposing admin, and permissionrequired mixins
from lifestudies.permissions import IsOwner

from .serializers import RollSerializer, AttendanceSerializer
from schedules.models import Schedule, Event
from leaveslips.models import IndividualSlip, GroupSlip
from terms.models import Term
from accounts.models import User, Trainee
from leaveslips.models import IndividualSlip
from leaveslips.forms import IndividualSlipForm

from guardian.decorators import permission_required_or_403
from guardian.shortcuts import get_objects_for_user



# class AttendancePersonal(views.PermissionRequiredMixin, TemplateView):
class AttendancePersonal(TemplateView):
    template_name = 'attendance/attendance_detail.html'
    context_object_name = 'context'


    #A good way to restrict permissions to views
    # permission_required = 'attendance.attendance_all'

    def get_context_data(self, **kwargs):
        context = super(AttendancePersonal, self).get_context_data(**kwargs)
        context['trainee'] = self.request.user.trainee
        context['schedule'] = Schedule.objects.filter(term=Term.current_term()).get(trainee=self.request.user.trainee)
        context['attendance'] = Roll.objects.filter(trainee=self.request.user.trainee).filter(event__term=Term.current_term())
        context['leaveslipform'] = IndividualSlipForm()
        context['leaveslips'] = chain(list(IndividualSlip.objects.filter(trainee=self.request.user.trainee).filter(events__term=Term.current_term())), list(GroupSlip.objects.filter(trainee=self.request.user.trainee).filter(start__gte=Term.current_term().start).filter(end__lte=Term.current_term().end)))
        return context


""" API Views """

class CurrentUserMixin(object):
    model = Trainee

    def get_object(self, *args, **kwargs):
        try:
            obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError:
            # SingleObjectMixin throws an AttributeError when no pk or slug
            # is present on the url. In those cases, we use the current user
            obj = self.request.user.trainee

        return obj

# Talk to David about this
# For AM's and TA's to see all records

# class AttendanceViewSet(viewsets.ModelViewSet):
#     serializer_class=AttendanceSerializer
#     permission_classes = [AttendanceAllorIsOwner]

#     def get_queryset(self):
#         return 


class AttendanceListAll(PermissionRequiredMixin, generics.ListAPIView):
    permission_required='attendance.attendance_all'
    login_url = 'attendancedetail'
    queryset = Trainee.objects.all()
    serializer_class=AttendanceSerializer

# AttendanceListAll redirects here
@permission_classes((AttendanceAllorIsOwner, )) #Possible TODO - make custom decorator that will take a login_url
class AttendanceDetail(generics.ListAPIView):
    serializer_class=AttendanceSerializer
    def get_queryset(self): 
        return [self.request.user.trainee] #Trainee.objects.all() #Trainee.objects.get(id=self.request.user.trainee)





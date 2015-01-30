# coding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tastypie.api import Api
from leaveslip_api.resources import IndividualSlipResource, GroupSlipResource, TraineeResource, TrainingAssistantResource, EventResource, RollResource

from rest_framework import routers

from accounts.views import *
from schedules.views import EventViewSet, ScheduleViewSet
from attendance.views import RollViewSet
from leaveslips.views import IndividualSlipViewSet, GroupSlipViewSet

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ap.views.home', name='home'),
    url(r'^accounts/login/$', login, name='login'),
	url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^dailybread/', include('dailybread.urls', namespace="dailybread")),
    url(r'^schedules/', include('schedules.urls', namespace="schedules")),
    url(r'^attendance/', include('attendance.urls', namespace="attendance")),
    url(r'^leaveslips/', include('leaveslips.urls', namespace="leaveslips")),
    url(r'^verse_parse/', include('verse_parse.urls', namespace="verse_parse")),
    url(r'^meal_seating/', include('meal_seating.urls')),
    url(r'^absent_trainee_roster/', include('absent_trainee_roster.urls', namespace="absent_trainee_roster")),
    url(r'^syllabus/', include('syllabus.urls', namespace="syllabus")),
    url(r'^lifestudies/', include('lifestudies.urls', namespace="lifestudies")),


    url(r'^adminactions/', include('adminactions.urls')), #django-adminactions pluggable app
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

# API urls
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'trainees', TraineeViewSet)
router.register(r'tas', TrainingAssistantViewSet)
router.register(r'events', EventViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'rolls', RollViewSet)
router.register(r'leaveslips', IndividualSlipViewSet)
router.register(r'groupleaveslips', GroupSlipViewSet)

urlpatterns += patterns('',
    url(r'^api/trainees/gender/(?P<gender>[BS])/$', TraineesByGender.as_view()),
    url(r'^api/trainees/term/(?P<term>[1234])/$', TraineesByTerm.as_view()),
    url(r'^api/trainees/team/(?P<pk>\d+)/$', TraineesByTeam.as_view()),
    url(r'^api/trainees/teamtype/(?P<type>\w+)/$', TraineesByTeamType.as_view()),
    url(r'^api/trainees/house/(?P<pk>\d+)/$', TraineesByHouse.as_view()),
    url(r'^api/trainees/locality/(?P<pk>\d+)/$', TraineesByLocality.as_view()),
    url(r'^api/trainees/hc/$', TraineesHouseCoordinators.as_view()),
    url(r'^api/', include(router.urls)),

    # tastypie leaveslips apis
    url(r'^api/', include(EventResource().urls)),
    url(r'^api/', include(GroupSlipResource().urls)),
    url(r'^api/', include(IndividualSlipResource().urls)),
    url(r'^api/', include(TrainingAssistantResource().urls)),
    url(r'^api/', include(TraineeResource().urls)),
    url(r'^api/', include(RollResource().urls)),

    #third party
    url(r'^explorer/', include('explorer.urls')),
    url(r'^select2/', include('django_select2.urls')),

)

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, url
from django.conf import settings

from schedules import views

urlpatterns = patterns('',
    url(r'schedule/$', views.SchedulePersonal.as_view(), name='schedule'),
    url(r'schedule/list/$', views.ScheduleList.as_view(), name='schedule-list'),
    url(r'schedule/(?P<pk>\d+)/$', views.ScheduleDetail.as_view(), name='schedule-detail'),
    url(r'schedule/create/$', views.ScheduleCreate.as_view(), name='schedule-create'),
    url(r'schedule/update/(?P<pk>\d+)/$', views.ScheduleUpdate.as_view(), name='schedule-update'),
    url(r'schedule/list/delete/(?P<pk>\d+)$', views.ScheduleDelete.as_view(), name='schedule-delete'),
    url(r'event/create/$', views.EventCreate.as_view(), name='event-create'),
    # url(r'event/detail/$', views.EventDetail.as_view(), name='event-detail'),
    url(r'event/list/$', views.EventList.as_view(), name='event-list'),
    url(r'event/(?P<pk>\d+)/$', views.EventDetail.as_view(), name='event-detail'),
    url(r'event/update/(?P<pk>\d+)/$', views.EventUpdate.as_view(), name='event-update'),
    url(r'event/list/delete/(?P<pk>\d+)$', views.EventDelete.as_view(), name='event-delete'),
    url(r'event/(?P<term>(Fa|Sp)\d{2})/$', views.TermEvents.as_view(), name='term-events'),
    url(r'^trainee-autocomplete/$', views.TraineeAutocomplete.as_view(), name='trainee-autocomplete'),
    url(r'^event-autocomplete/$', views.EventAutocomplete.as_view(), name='event-autocomplete'),
    url(r'^schedule-autocomplete/$', views.ScheduleAutocomplete.as_view(), name='schedule-autocomplete'),
)

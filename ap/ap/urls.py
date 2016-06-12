# coding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import login as auth_login
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import routers

from accounts.views import *
from schedules.views import EventViewSet, ScheduleViewSet, AllEventViewSet, AllScheduleViewSet
from attendance.views import RollViewSet, AllRollViewSet
from leaveslips.views import IndividualSlipViewSet, GroupSlipViewSet, AllIndividualSlipViewSet, AllGroupSlipViewSet
from books.views import BooksViewSet
from lifestudies.views import DisciplineSummariesViewSet
from attendance.views import AttendanceViewSet, AllAttendanceViewSet
from seating.views import ChartViewSet, SeatViewSet
from terms.views import TermViewSet

from rest_framework_nested import routers
from rest_framework_bulk.routes import BulkRouter

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ap.views.home', name='home'),
    url(r'^accounts/login/$', auth_login, name='login'),
	url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^dailybread/', include('dailybread.urls', namespace="dailybread")),
    url(r'^badges/', include('badges.urls', namespace="badges")),
    url(r'^schedules/', include('schedules.urls', namespace="schedules")),
    url(r'^attendance/', include('attendance.urls', namespace="attendance")),
    url(r'^leaveslips/', include('leaveslips.urls', namespace="leaveslips")),
    url(r'^verse_parse/', include('verse_parse.urls', namespace="verse_parse")),
    url(r'^meal_seating/', include('meal_seating.urls')),
    url(r'^absent_trainee_roster/', include('absent_trainee_roster.urls', namespace="absent_trainee_roster")),
    url(r'^syllabus/', include('syllabus.urls', namespace="syllabus")),
    url(r'^lifestudies/', include('lifestudies.urls', namespace="lifestudies")),
    url(r'^seating/', include('seating.urls', namespace='seating')),
    url(r'^exams/', include('exams.urls', namespace="exams")),
    url(r'^web_access/', include('web_access.urls', namespace="web_access")),
    url(r'^bible_tracker/', include('bible_tracker.urls', namespace='bible_tracker')),

    # admin urls
    url(r'^adminactions/', include('adminactions.urls')), #django-adminactions pluggable app
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = BulkRouter()
router.register(r'users', UserViewSet)
router.register(r'trainees', TraineeViewSet, base_name='trainees')
router.register(r'events', EventViewSet)
router.register(r'allevents', AllEventViewSet, base_name='allevents')
router.register(r'schedules', ScheduleViewSet)
router.register(r'allschedules', AllScheduleViewSet, base_name='allschedules')
router.register(r'rolls', RollViewSet)
router.register(r'allrolls', AllRollViewSet, base_name='allrolls')
router.register(r'individualslips', IndividualSlipViewSet)
router.register(r'allindividualleaveslips', AllIndividualSlipViewSet, base_name='allindividualslips')
router.register(r'groupslips', GroupSlipViewSet)
router.register(r'allgroupslips', AllGroupSlipViewSet, base_name='allgroupslips')
router.register(r'books', BooksViewSet)
router.register(r'summaries', DisciplineSummariesViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'allattendance', AllAttendanceViewSet, base_name='allattendance')
router.register(r'charts', ChartViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'terms', TermViewSet)

attendance_router = routers.NestedSimpleRouter(router, r'attendance', lookup='attendance')
attendance_router.register(r'rolls', RollViewSet, base_name='rolls')
rolls_router = routers.NestedSimpleRouter(attendance_router, r'rolls', lookup='rolls')
attendance_router.register(r'events', EventViewSet, base_name='events')
events_router = routers.NestedSimpleRouter(attendance_router, r'events', lookup='events')
attendance_router.register(r'schedules', ScheduleViewSet, base_name='schedules')
schedules_router = routers.NestedSimpleRouter(attendance_router, r'schedules', lookup='schedules')
attendance_router.register(r'individualslips', IndividualSlipViewSet, base_name='individualslips')
leaveslips_router = routers.NestedSimpleRouter(attendance_router, r'individualslips', lookup='individualslips')
attendance_router.register(r'groupslips', GroupSlipViewSet, base_name='groupslips')
groupleaveslips_router = routers.NestedSimpleRouter(attendance_router, r'groupslips', lookup='groupslips')

urlpatterns += patterns('',
    url(r'^api/trainees/gender/(?P<gender>[BS])/$', TraineesByGender.as_view()),
    url(r'^api/trainees/term/(?P<term>[1234])/$', TraineesByTerm.as_view()),
    url(r'^api/trainees/team/(?P<pk>\d+)/$', TraineesByTeam.as_view()),
    url(r'^api/trainees/teamtype/(?P<type>\w+)/$', TraineesByTeamType.as_view()),
    url(r'^api/trainees/house/(?P<pk>\d+)/$', TraineesByHouse.as_view()),
    url(r'^api/trainees/locality/(?P<pk>\d+)/$', TraineesByLocality.as_view()),
    url(r'^api/trainees/hc/$', TraineesHouseCoordinators.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(attendance_router.urls)),
    #third party
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^select2/', include('django_select2.urls')),
)

urlpatterns += staticfiles_urlpatterns()

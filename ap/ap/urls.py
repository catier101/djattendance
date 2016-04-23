# coding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib.auth.decorators import permission_required

from rest_framework import routers

from accounts.views import *
from schedules.views import EventViewSet, ScheduleViewSet
from attendance.views import AttendanceListAll, AttendanceDetail
from leaveslips.views import IndividualSlipViewSet, GroupSlipViewSet
from books.views import BooksViewSet
from lifestudies.views import DisciplineSummariesViewSet
from house_forms.views import LinenRequestListAll, LinenRequestListHC

from attendance.admin import admin_site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ap.views.home', name='home'),
    url(r'^accounts/login/$', login, name='login'),
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
    # admin urls
    url(r'^adminactions/', include('adminactions.urls')), #django-adminactions pluggable app
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls), name="admin"),
    # HC Admin site
    url(r'^hcadmin/', admin_site.urls),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# API urls
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'trainees', TraineeViewSet)
router.register(r'tas', TrainingAssistantViewSet)
router.register(r'events', EventViewSet)
router.register(r'schedules', ScheduleViewSet)
# router.register(r'rolls', RollListAPIView)
# router.register(r'rolls/?P<pk>\d+)/$', RollDetail)
# router.register(r'rolls', RollViewSet)
router.register(r'leaveslips', IndividualSlipViewSet)
router.register(r'groupleaveslips', GroupSlipViewSet)
router.register(r'books', BooksViewSet)
router.register(r'summaries', DisciplineSummariesViewSet)
# router.register(r'attendance', AttendanceViewSet)

urlpatterns += patterns('',
    url(r'^api/trainees/gender/(?P<gender>[BS])/$', TraineesByGender.as_view()),
    url(r'^api/trainees/term/(?P<term>[1234])/$', TraineesByTerm.as_view()),
    url(r'^api/trainees/team/(?P<pk>\d+)/$', TraineesByTeam.as_view()),
    url(r'^api/trainees/teamtype/(?P<type>\w+)/$', TraineesByTeamType.as_view()),
    url(r'^api/trainees/house/(?P<pk>\d+)/$', TraineesByHouse.as_view()),
    url(r'^api/trainees/locality/(?P<pk>\d+)/$', TraineesByLocality.as_view()),
    url(r'^api/trainees/hc/$', TraineesHouseCoordinators.as_view()),
    # url(r'^api/attendance/(?P<pk>\d+)/$', AttendanceDetail.as_view(), name='attendancedetail'),
    url(r'^api/attendances/$', AttendanceDetail.as_view(), name='attendancedetail'),
    url(r'^api/attendance/$', AttendanceListAll.as_view()),
    url(r'^api/house_forms/linen_requests_p/$', LinenRequestListAll.as_view()),
    url(r'^api/house_forms/linen_requests/$', LinenRequestListHC.as_view()),
    url(r'^api/', include(router.urls)),

    #third party
    url(r'^explorer/', include('explorer.urls')),
    url(r'^select2/', include('django_select2.urls')),
)

urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.DisciplineListView.as_view(), name='discipline_list'),
    url(r'^discipline-report$', views.DisciplineReportView.as_view(),
        name='discipline_report'),
    url(r'^(?P<pk>\d+)/create-summary$', views.SummaryCreateView.as_view(),
        name='summary_create'),
    url(r'^(?P<pk>\d+)/detail-summary$', views.SummaryUpdateView.as_view(),
        name='summary_detail'),
    url(r'^(?P<pk>\d+)/approve-summary$', views.SummaryApproveView.as_view(),
        name='summary_approve'),
    url(r'^create_discipline-house$', views.CreateHouseDiscipline.as_view(),
        name='discipline_house'),
    url(r'^create-discipline$', views.DisciplineCreateView.as_view(),
        name='discipline_create'),
    url(r'^(?P<pk>\d+)/detail-discipline$', views.DisciplineDetailView.as_view(),
        name='discipline_detail'),
    url(r'^(?P<period>\d+)/attendance-assign$', views.AttendanceAssign.as_view(),
        name='attendance_assign'),
)

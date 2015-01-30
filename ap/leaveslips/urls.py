from django.conf.urls import patterns, url

from leaveslips import views

urlpatterns = patterns('',
    url(r'individual/create/$', views.IndividualSlipCreate.as_view(), name='individual-create'),
    url(r'individual/(?P<pk>\d+)$', views.IndividualSlipDetail.as_view(), name='individual-detail'),
    url(r'individual/update/(?P<pk>\d+)$', views.IndividualSlipUpdate.as_view(), name='individual-update'),
    url(r'individual/delete/(?P<pk>\d+)$', views.IndividualSlipDelete.as_view(), name='individual-delete'),

    url(r'group/create/$', views.GroupSlipCreate.as_view(), name='group-create'),
    url(r'group/(?P<pk>\d+)$', views.GroupSlipDetail.as_view(), name='group-detail'),
    url(r'group/update/(?P<pk>\d+)$', views.GroupSlipUpdate.as_view(), name='group-update'),
    url(r'group/delete/(?P<pk>\d+)$', views.GroupSlipDelete.as_view(), name='group-delete'),

    url(r'^$',views.LeaveSlipList.as_view(), name='leaveslips-list'),

)

#     url(r'schedule/list/$', views.ScheduleList.as_view(), name='schedule-list'),

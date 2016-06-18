from django.conf.urls import patterns, url

from web_access import views, utils
from web_access.models import WebRequest

urlpatterns = patterns(
    '',
    url(r'^$', views.WebRequestList.as_view(), name='web_access-list'),
    url(r'^create$', views.WebAccessCreate.as_view(model=WebRequest, success_url='/web_access/'), name='web_access-create'),
    url(r'^detail/(?P<pk>\d+)$', views.WebAccessDetail.as_view(), name='web_access-detail'),
    url(r'^update/(?P<pk>\d+)$', views.WebAccessUpdate.as_view(model=WebRequest, success_url='/web_access/'), name='web_access-update'),
    url(r'^delete/(?P<pk>\d+)$', views.WebAccessDelete.as_view(model=WebRequest, success_url='/web_access/'), name='web_access-delete'),
    url(r'^ta/update/(?P<pk>\d+)$', views.TAWebAccessUpdate.as_view(model=WebRequest, success_url='/web_access/ta'), name='web_access-update-ta'),
    url(r'^ta$', views.TAWebRequestList.as_view(), name='ta-web_access-list'),
    url(r'^(?P<status>[APFDS])/(?P<id>\d+)$', views.modify_status, name='modify-status'),
    url(r'^(?P<minutes>\d+)/(?P<id>\d+)$', utils.startAccess, name='start-access'),
)

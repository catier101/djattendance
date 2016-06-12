from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = patterns(
    '',
    url(regex=r'^(?P<pk>\d+)$', view=views.UserDetailView.as_view(), name='user_detail'),
    url(regex=r'^events$', view=views.EventsListView.as_view(), name='events_list'),
    url(regex=r'^update/(?P<pk>\d+)$', view=views.UserUpdateView.as_view(), name='user_update'),
    url(regex=r'^email/update/(?P<pk>\d+)$', view=views.EmailUpdateView.as_view(), name='email_change'),
    url(regex=r'^password/change$', view=auth_views.password_change,
        kwargs={'template_name': 'accounts/password_change_form.html',
                'current_app': 'accounts'},
        name='password_change'),
    url(regex=r'^password/change/done$', view=auth_views.password_change_done,
        kwargs={'template_name': 'accounts/password_change_done.html',
                'current_app': 'accounts'},
        name='password_change_done'),
    url(regex=r'^switch$', view=views.SwitchUserView.as_view(), name='switch_user'),
)

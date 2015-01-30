from django.conf.urls import patterns, url

#from django.contrib.auth.decorators import permission_required
#from absent_trainee_roster.views import absent_trainee_form

from absent_trainee_roster import views

urlpatterns = patterns('',
	#url(r'^absent_trainee_form/$', permission_required('is_hc')(absent_trainee_form.as_view()), name='absent_trainee_form'),
	url(r'^absent_trainee_form/$', views.absent_trainee_form, name='absent_trainee_form'),
)
from django.conf.urls import patterns, url
from verse_parse import views

urlpatterns = patterns('',
	url(r'^$', views.upload_file, name='verse_parse'),
)
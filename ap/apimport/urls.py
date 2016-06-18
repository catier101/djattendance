from django.conf.urls import patterns, url
from apimport import views


urlpatterns = patterns(
    '',
    url(r'term-details$', views.CreateTermView.as_view(), name='term_details'),
    url(r'process-csv$', views.ProcessCsvData.as_view(), name='process_csv'),
    url(r'save-data$', views.save_data, name='save_data')
)
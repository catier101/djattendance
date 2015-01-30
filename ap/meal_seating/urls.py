from django.conf.urls import patterns, url

from meal_seating import views

urlpatterns = patterns('',
    url(r'newseating/',
        views.newseats),
    url(r'viewlist/',
        views.seattables),
    url(r'mealsignin/',
        views.signin),
)

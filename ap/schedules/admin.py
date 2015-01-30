from django.contrib import admin
from .models import Event, EventGroup, Schedule, ScheduleTemplate

admin.site.register(Event)
admin.site.register(EventGroup)
admin.site.register(Schedule)
admin.site.register(ScheduleTemplate)

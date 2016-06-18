from django.contrib import admin
from schedules.models import *
from .models import Event, Schedule, Class

class ClassAdmin(admin.ModelAdmin):
  exclude = ['type']

  # Automatically type class event objects saved.
  def save_model(self, request, obj, form, change):
    obj.type = 'C'
    obj.save()

admin.site.register(Event)
admin.site.register(Schedule)
admin.site.register(Class, ClassAdmin)
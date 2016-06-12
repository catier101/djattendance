from django.contrib import admin

from .models import Chart, Seat, Partial

admin.site.register(Chart)
admin.site.register(Seat)
admin.site.register(Partial)

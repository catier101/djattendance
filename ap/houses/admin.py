from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from accounts.models import Trainee
from houses.models import House, Room, Bunk
from aputils.models import Address

admin.site.register(House)
admin.site.register(Room)
admin.site.register(Bunk)

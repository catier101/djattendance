from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from accounts.models import Trainee
from houses.models import House, Room, Bunk
from aputils.models import Address

# class HCAdminSite(AdminSite):
# 	site_header = "House Coordinator Administration"

# admin_site = HCAdminSite(name='hc_admin')
# admin_site.register(Bunk)
# admin_site.register(House)
# admin_site.register(Room)

admin.site.register(House)
admin.site.register(Room)
admin.site.register(Bunk)

from django.contrib import admin
from django.contrib.admin import AdminSite
from guardian.admin import GuardedModelAdmin
from .models import Roll
from django.contrib.auth.models import Permission

class HCModelAdmin(AdminSite):
	site_header = "HC Admin"

admin_site = HCModelAdmin(name='hcadmin')



admin.site.register(Roll)
admin.site.register(Permission)


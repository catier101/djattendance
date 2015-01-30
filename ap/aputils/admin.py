from django import forms
from django.contrib import admin

from aputils.models import Country, City, Address, Vehicle, EmergencyInfo

class AddressAdminForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.order_by('name'))

    class Meta:
        model = Address


class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = (
        'address1', 
        'address2', 
        'city', 
        'zip_code', 
        'zip4', 
        'details'
    )
    ordering = ('address1', 'address2',)
    search_fields = ['address1', 'address2', 'zip_code', 'zip4']


class CityAdminForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.order_by('name'))

    class Meta:
        model = City


class CityAdmin(admin.ModelAdmin):
    form = CityAdminForm
    list_display = (
        'name',
        'state',
        'country'
    )
    ordering = ('country', 'state', 'name',)
    search_fields = ['name', 'state']


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code'
    )
    ordering = ('name', 'code',)
    search_fields = ['name', 'code']


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'license_plate',
        'color',
        'make',
        'model',
        'year',
        'capacity',
    )
    ordering = ('make', 'model', 'color', 'license_plate',)
    search_fields = ['make', 'model', 'color', 'license_plate', 'capacity']


class VehicleInline(admin.TabularInline):
    model = Vehicle
    fk_name = 'trainee'


class EmergencyInfoInline(admin.TabularInline):
    model = EmergencyInfo
    fk_name = 'trainee'
    verbose_name = 'emergency contact'
    verbose_name_plural = 'emergency contacts'
    extra = 1


admin.site.register(Address, AddressAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(EmergencyInfo)

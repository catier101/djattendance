# from django.contrib import admin
# from django import forms

# from services.models import Category, Service, Period, ServiceWorkerGroup


# class CategoryAdminForm(admin.ModelAdmin):
#   list_display = ('name', 'description',)
#   # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#   search_fields = ('name', 'description',)
#   ordering = ('description',)

#   class Meta:
#     model = Category
#     fields = '__all__'


# class ServiceAdminForm(admin.ModelAdmin):
#   list_display = ('name', 'category', 'active', 'designated', 
#                   'gender', 'workers_required', 'weekday')
#   # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#   search_fields = ('name', 'category__name',)
#   ordering = ('name',)
#   exclude= ('permissions',)
#   # Allows django admin to duplicate record
#   save_as = True

#   class Meta:
#     model = Service
#     fields = '__all__'


# class ServiceWorkerGroupAdminForm(admin.ModelAdmin):
#   list_display = ('service', 'worker_group', 'workers_required', 'workload', 
#                   'role', 'gender')
#   # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#   search_fields = ('service', 'workload',)
#   ordering = ('service',)
#   # exclude= ('permissions',)
#   # Allows django admin to duplicate record
#   save_as = True

#   class Meta:
#     model = Service
#     fields = '__all__'



# admin.site.register(Category, CategoryAdminForm)
# admin.site.register(Service, ServiceAdminForm)
# admin.site.register(ServiceWorkerGroup, ServiceWorkerGroupAdminForm)
# admin.site.register(Period)

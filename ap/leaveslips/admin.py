from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from leaveslips.models import LeaveSlip, IndividualSlip, GroupSlip



class ApproveFilter(SimpleListFilter):
	#Filters to separate approved from unfinalized leaveslips
	title = _('Approved')

	parameter_name = 'approved'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each tuple is the coded value
		for the option that will appear in the URL query. The second element is the human-
		readable name for the option that will appear in the right sidebar.
		"""
		return (
			('Approved', _('Approved')),
			('Pending', _('Pending')),
		)

	def queryset(self, request, queryset):
		"""
		"""
		if self.value() == 'Approved':
			"""queryset of approved leaveslips """
			q=queryset.filter(status='A')
			return q

		if self.value() == 'Pending':
			"""queryset of pending leaveslips """
			q=queryset.exclude(status='A')
			return q

def make_approved(modeladmin, request, queryset):
	queryset.update(status='A')
make_approved.short_description = "Approve selected leaveslips"


def mark_for_fellowship(modeladmin, request, queryset):
	queryset.update(status='F')
make_approved.short_description = "Mark selected leaveslips for fellowship"


def make_denied(modeladmin, request, queryset):
	queryset.update(status='D')
make_approved.short_description = "Deny selected leaveslips"


class IndividualSlipAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('trainee',('type', 'status',), 'description', 'comments', ('texted', 'informed',),'events','TA',)
        }),
    )
    list_display = ('pk', 'trainee','status','type','submitted','late','TA','finalized')
    actions = [make_approved, mark_for_fellowship, make_denied]
    list_filter = ( ApproveFilter,'TA',)
    search_fields = ['trainee__account__firstname', 'trainee__account__lastname'] #to search up trainees


# Register your models here.
admin.site.register(IndividualSlip, IndividualSlipAdmin)
admin.site.register(GroupSlip)

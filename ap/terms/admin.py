from django.contrib import admin
from terms.models import Term

class TermAdmin(admin.ModelAdmin):
    ordering = ['start']

admin.site.register(Term, TermAdmin)

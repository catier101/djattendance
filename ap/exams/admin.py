from django.contrib import admin
from exams.models import Exam, Section, Session
from django.forms import Textarea
from django.db import models

class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ('total_score', 'section_count',)

admin.site.register(Exam, ExamAdmin)
admin.site.register(Section)
admin.site.register(Session)
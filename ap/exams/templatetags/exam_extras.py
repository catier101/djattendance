from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter(name='lookup')
def lookup(d, key):
    return d[key]

@register.filter(name='is_taking_exam')
def is_taking_exam(role):
    if role == "Take" or role =="Retake":
        return True
    return False

@register.filter(name='link_text')
def link_text(exam):
    if exam.is_graded:
        return exam.grade
    return "Grade exam"

register.filter('lookup', lookup)
register.filter('is_taking_exam', is_taking_exam)
register.filter('link_text', link_text)
from django import template
from aputils.utils import is_trainee, is_TA
from django.core.urlresolvers import reverse

register = template.Library()

register.filter('is_trainee', is_trainee)
register.filter('is_TA', is_TA)


from django import template
from aputils.utils import is_trainee, is_TA

register = template.Library()

register.filter('is_trainee', is_trainee)

register.filter('is_TA', is_TA)


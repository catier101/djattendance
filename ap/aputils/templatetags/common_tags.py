from django import template
from aputils.utils import is_trainee, is_TA

from aputils.permissions import SubMenuItem, MenuItem 

register = template.Library()

register.filter('is_trainee', is_trainee)
register.filter('is_TA', is_TA)

#This tag generates the current menu
@register.assignment_tag(takes_context=True)
def generate_current_menu(context):
	#For every 'current' item that needs to appear in the side-bar, ie exams to be taken, iterim intentions form, exit interview, etc, the context variable needs to be added to the context, and the menu item can be added here as follows
	current_menu = MenuItem(name = 'Current', 
		trainee_only=[SubMenuItem(name="Take Exam", url='exams:list', condition = context['exams_available'])])  
	current_menu = context['user_menu'] + [current_menu]
	return current_menu


#Needs to check a certain condition. True? Relevant menu? 
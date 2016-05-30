from django.contrib.auth.models import Permission #do I need this? 
import collections


def namedtuple_d(typename, field_names, default_values=()):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

def SubMenuItem(name, permission = None, url = '#', condition = None):
	return namedtuple_d('SubMenuItem', 'name permission url condition')(name = name, permission = permission, url = url, condition = condition)

def MenuItem(name, ta_only = None, trainee_only = None, common = None, specific = None):
	return namedtuple_d('MenuItem', 'name ta_only trainee_only common specific')(name = name, ta_only = ta_only, trainee_only = trainee_only, common = common, specific = specific)

# site: http://stackoverflow.com/questions/11351032/named-tuple-and-optional-keyword-arguments

def user_menu(request):

	# Set conditions here
	exams_available = True

	attendance_menu = MenuItem(name='Attendance', 
		ta_only=[SubMenuItem(name='Create Event', url='schedules:event-create')], 
		trainee_only=[SubMenuItem(name='View Schedule', url='schedules:schedule'), SubMenuItem(name='Personal Attendance', url='attendance:attendance-submit'), SubMenuItem(name='View Personal Leaveslips', url='leaveslips:leaveslips-list')], 
		common=[SubMenuItem(name='Submit Individual Leaveslips', url='leaveslips:individual-create'), SubMenuItem(name='Submit Group Leaveslips', url='leaveslips:group-create')], 
		specific=[SubMenuItem(name='View Trainee Leaveslips', permission='attendance.add_roll', url='leaveslips:ta-leaveslip-list')])
	discipline_menu = MenuItem(name ='Discipline', 
		common =[SubMenuItem(name='Life Studies', url='lifestudies:discipline_list'), SubMenuItem(name='Class Notes', url='#')])
	exam_menu = MenuItem(name = 'Exams',  
		specific = [SubMenuItem(name="Create Exam", permission='exams.add_exam', url='exams:submit')])
	requests_menu = MenuItem(name= 'Requests', 
		common=[SubMenuItem(name='A/V Requests', url='#'), SubMenuItem(name='Maintenance Requests', url='#'), SubMenuItem(name='Room Reservations', url='#'), SubMenuItem(name='Web Access Requests', url='web_access:web_access-list')])
	misc_menu = MenuItem(name="Misc.", 
		common=[SubMenuItem(name='Announcements', url='#'), SubMenuItem(name='Bible Reading Tracker', url='#')],
		specific=[SubMenuItem(name='Badges', permission='badges.add_badge', url='badges:badges_list'), SubMenuItem(name="Absent Trainee Roster", permission='attendance.add_roll', url='absent_trainee_roster:absent_trainee_form'), SubMenuItem(name='Meal Seating', permission='meal_seating.add_table', url='meal_seating.views.newseats')])

	# exams_available = True
	# conditions = (exams_available)


# I want to be able to write a list of conditions here and then check on these conditions in base.html
# Idea - have a conditional menu, pass it in as another dict item. 

	menu = [attendance_menu, discipline_menu, requests_menu, exam_menu, misc_menu]
	# menu = [attendance_menu, discipline_menu, requests_menu, misc_menu]
	return dict(user_menu = menu, exams_available = exams_available)

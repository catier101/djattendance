from django.contrib.auth.models import Permission
from collections import namedtuple

def user_menu(request):
	MenuItem = namedtuple('MenuItem', 'name ta_only trainee_only common specific')
	SubMenuItem = namedtuple('SubMenuItem', 'name url')
	SpecificPermItem = namedtuple('SpecificPermItem', 'name permission url')

	attendance_menu = MenuItem(name='Attendance', 
		ta_only=[SubMenuItem(name='Create Event', url='schedules:event-create')], 
		trainee_only=[SubMenuItem(name='View Schedule', url='schedules:schedule'), SubMenuItem(name='Personal Attendance', url='attendance:attendance-submit'), SubMenuItem(name='View Personal Leaveslips', url='leaveslips:leaveslips-list')], 
		common=[SubMenuItem(name='Submit Individual Leaveslips', url='leaveslips:individual-create'), SubMenuItem(name='Submit Group Leaveslips', url='leaveslips:group-create')], 
		specific=[SpecificPermItem(name='View Trainee Leaveslips', permission='attendance.add_roll', url='leaveslips:ta-leaveslip-list')])
	discipline_menu = MenuItem(name ='Discipline', 
		ta_only=[], 
		trainee_only=[], 
		common =[SubMenuItem(name='Life Studies', url='lifestudies:discipline_list'), SubMenuItem(name='Class Notes', url='#')], 
		specific=[])
	exam_menu = MenuItem(name = 'Exams', 
		ta_only=[], 
		trainee_only=[SubMenuItem(name="Take Exam", url='exams:take')], 
		common=[], 
		specific = [SpecificPermItem(name="Create Exam", permission='exams.add_exam', url='exams:submit')])
	requests_menu = MenuItem(name= 'Requests', 
		ta_only=[], 
		trainee_only=[], 
		common=[SubMenuItem(name='A/V Requests', url='#'), SubMenuItem(name='Maintenance Requests', url='#'), SubMenuItem(name='Room Reservations', url='#'), SubMenuItem(name='Web Access Requests', url='web_access:web_access-list')], 
		specific=[])
	misc_menu = MenuItem(name="Misc.", 
		ta_only=[], 
		trainee_only=[], 
		common=[SubMenuItem(name='Announcements', url='#'), SubMenuItem(name='Bible Reading Tracker', url='#')],
		specific=[SpecificPermItem(name='Badges', permission='badges.add_badge', url='badges:badges_list'), SpecificPermItem(name="Absent Trainee Roster", permission='attendance.add_roll', url='absent_trainee_roster:absent_trainee_form'), SpecificPermItem(name='Meal Seating', permission='meal_seating.add_table', url='meal_seating.views.newseats')])

	menu = [attendance_menu, discipline_menu, exam_menu, requests_menu, misc_menu]
	return dict(user_menu = menu)

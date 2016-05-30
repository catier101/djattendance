from .models import Exam
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

# site: http://stackoverflow.com/questions/11351032/named-tuple-and-optional-keyword-arguments


MenuItem = namedtuple_d('MenuItem', 'name ta_only trainee_only common specific')
SubMenuItem = namedtuple_d('SubMenuItem', 'name permission url')

exam_menu = MenuItem(name = 'Exams', 
	# trainee_only=[SubMenuItem(name="Take Exam", url='exams:list')], 
	specific = [SubMenuItem(name="Create Exam", permission='exams.add_exam', url='exams:submit')])

def exams_available(request):
	if Exam.objects.filter(is_open=True).count() > 0:
		return {'exams_available' : True, 'exam_menu': exam_menu}
	else:
		return {'exams_available': False }



from .models import Exam

def exams_available(request):
	return {'exams_available' : Exam.objects.filter(is_open=True).count() > 0}



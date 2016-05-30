from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from dailybread.models import Portion
from schedules.models import Schedule
from terms.models import Term
from accounts.models import Trainee

from aputils.utils import is_trainee, is_TA, trainee_from_user

@login_required
def home(request):
    data = {'daily_nourishment': Portion.today(),
            'user': request.user}

    if is_trainee(request.user):
        trainee = trainee_from_user(request.user)
        try:
            data['schedule'] = trainee.schedule.get(term=Term.current_term())
        except ObjectDoesNotExist:
            pass
        for discipline in trainee.discipline_set.all():
            if discipline.get_num_summary_due() > 0:
                messages.warning(request, 'Life Study Summary Due for {infraction}. <a href="/lifestudies">Still need: {due}</a>'.format(infraction=discipline.infraction, due=discipline.get_num_summary_due()))

    elif is_TA(request.user):
        #do stuff to TA
        pass
    else:
        #do stuff to other kinds of users
        pass

    return render(request, 'index.html', dictionary=data)

def base_example(request):
	return render(request, 'base_example.html')

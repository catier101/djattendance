from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from meal_seating.models import Table
from accounts.models import User
from datetime import date, timedelta


@csrf_protect
def seattables(request):
    filterchoice = request.POST['Filter']
    genderchoice = request.POST['Gender']

    trainees = User.objects.all().filter(is_active=1, gender=genderchoice).order_by(filterchoice)[:50]

    mydict = Table.seatinglist(trainees,genderchoice)

    return render(request, 'detail.html', {'mydict' : mydict})

def newseats(request):
    return render(request, 'newseating.html')

def signin(request):
    trainees = User.objects.all().filter(is_active=1).order_by("lastname")[:50]
    startdate = date.today()
    two_week_datelist = []
    for x in range(0,14):
        mydate = startdate + timedelta(days=x)
        two_week_datelist.append(format(mydate))
    return render(request, 'mealsignin.html', {'trainees' : trainees, 'start_date' : startdate, "two_week_datelist" : two_week_datelist})
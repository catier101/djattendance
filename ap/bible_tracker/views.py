from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader
#from django.views.decorators.csrf import csrf_exempt

from terms.models import Term
from .models import BibleReading, User
from verse_parse.bible_re import *
import json
import datetime

def changeWeek(request):
    my_user = request.user;
    if request.is_ajax():
        week_id = request.GET['week'] 
        current_term = Term.current_term()
        term_id = current_term.id
        term_week_code = str(term_id) + "_" + str(week_id) 
        try:
            trainee_weekly_reading = BibleReading.objects.get(trainee = my_user).weekly_reading_status[term_week_code]
            print trainee_weekly_reading
            json_weekly_reading = json.loads(trainee_weekly_reading)
            weekly_status = str(json_weekly_reading['status'])
        except:
            weekly_status="_______"
        return HttpResponse(weekly_status)

def updateStatus(request):
    my_user = request.user;
    if request.is_ajax():
        week_id = request.POST['week_id'] 
        weekly_status = request.POST['weekly_status']
        
        current_term = Term.current_term()
        term_id = current_term.id
        term_week_code = str(term_id) + "_" + str(week_id) 
        
        try:
            trainee_bible_reading = BibleReading.objects.get(trainee = my_user)

        except:
            trainee_bible_reading = BibleReading(trainee = my_user, weekly_reading_status = {term_week_code:"{\"status\": \"_______\", \"finalized\": \"N\"}"}, books_read = {} ) 

        if term_week_code not in trainee_bible_reading.weekly_reading_status: 
            trainee_bible_reading.weekly_reading_status[term_week_code] = "{\"status\": \"_______\", \"finalized\": \"N\"}"

        trainee_weekly_reading = trainee_bible_reading.weekly_reading_status[term_week_code]
        json_weekly_reading = json.loads(trainee_weekly_reading)
        json_weekly_reading['status'] = weekly_status
        hstore_weekly_reading = json.dumps(json_weekly_reading)
        trainee_bible_reading.weekly_reading_status[term_week_code] = hstore_weekly_reading
        trainee_bible_reading.save()

        return HttpResponse(weekly_status)


def index(request):
    my_user = request.user;
    #AJAX for first-year and second-year bible reading 
    if request.is_ajax():
        try:
            #Setup
            isChecked = request.POST['checked']     
            myYear = request.POST['year']

            trainee_bible_reading = BibleReading.objects.get(trainee = my_user)
            book_code = request.POST['year'] + "_" + request.POST['book']

            #If checked, adds book to the database
            if isChecked == "true":
                trainee_bible_reading.books_read[book_code] = 'Y'
                trainee_bible_reading.save()
                
            #If not checked, deletes book from the database
            else:
                del trainee_bible_reading.books_read[book_code]
                trainee_bible_reading.save()
            
            #Calculates how much the progress bar changes for both first-year and second-year bible reading 
            user_checked_list = BibleReading.objects.get(trainee = my_user).books_read
            bible_books = testaments['ot'] + testaments['nt']
            bible_books_list = [book[0] for book in bible_books]

            if( myYear == "1" ):
                first_year_checked_list = [int(book_code.split("_")[1]) for book_code in user_checked_list.keys() if book_code.startswith('1_')]
                first_year_progress = 0;
                for checked_book in first_year_checked_list:
                    first_year_progress = first_year_progress + sum([int(chapter_verse_count) for chapter_verse_count in bible_books[checked_book][3]])
                first_year_progress = int(float(first_year_progress)/31102.0 * 100)
                return HttpResponse(str(first_year_progress))
            else:
                second_year_checked_list = [int(book_code.split("_")[1]) for book_code in user_checked_list.keys() if book_code.startswith('2_')]
                second_year_progress = 0;
                for checked_book in second_year_checked_list:
                    second_year_progress = second_year_progress + sum([int(chapter_verse_count) for chapter_verse_count in bible_books[checked_book][3]])
                second_year_progress = int(float(second_year_progress)/7957.0 * 100);
                return HttpResponse(str(second_year_progress))
        except:
            selected_book = 0
    else:
        selected_book = 0

    #Default for Daily Bible Reading
    current_term = Term.current_term()
    term_id = current_term.id
    base = current_term.start
    start_date = current_term.start.strftime('%Y%m%d')

    #Default for First-year and Second-year bible reading
    bible_books = testaments['ot'] + testaments['nt']
    bible_books_list = [book[0] for book in bible_books]

    try:
        user_checked_list = BibleReading.objects.get(trainee = my_user).books_read
    except:
        user_checked_list = {}

    first_year_checked_list = [int(book_code.split("_")[1]) for book_code in user_checked_list.keys() if book_code.startswith('1_')]
    second_year_checked_list = [int(book_code.split("_")[1]) for book_code in user_checked_list.keys() if book_code.startswith('2_')]
    
    first_year_progress = 0;
    for checked_book in first_year_checked_list:
        first_year_progress = first_year_progress + sum([int(chapter_verse_count) for chapter_verse_count in bible_books[checked_book][3]])
    first_year_progress = int(float(first_year_progress)/31102.0 * 100)

    second_year_progress = 0;
    for checked_book in second_year_checked_list:
        second_year_progress = second_year_progress + sum([int(chapter_verse_count) for chapter_verse_count in bible_books[checked_book][3]])
    second_year_progress = int(float(second_year_progress)/7957.0 * 100)

    current_date = datetime.date.today()
    current_week = Term.reverse_date(current_term, current_date)[0]
    term_week_code = str(term_id) + "_" + str(current_week) 

    try:
        weekly_reading = BibleReading.objects.get(trainee = my_user).weekly_reading_status[term_week_code]
        json_weekly_reading = json.loads(weekly_reading)
        weekly_status = str(json_weekly_reading['status'])
    except:
        trainee_bible_reading = BibleReading(trainee = my_user, weekly_reading_status = {term_week_code:"{\"status\": \"_______\", \"finalized\": \"N\"}"}, books_read = {} ) 
        trainee_bible_reading.save()
        weekly_status="_______"

    #Send data to the template!!!
    template = loader.get_template('bible_tracker/index.html')
    context = RequestContext(request, {
        'bible_books_list': bible_books_list,
        'first_year_checked_list': first_year_checked_list,
        'second_year_checked_list': second_year_checked_list,
        'first_year_progress': first_year_progress,
        'second_year_progress': second_year_progress,
        'weekly_status': weekly_status,
        'current_week':current_week,
        'start_date':start_date,
    })
    return HttpResponse(template.render(context))

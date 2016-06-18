import os
import sys
import os

from datetime import datetime, timedelta
import json

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from terms.models import Term

from .forms import DateForm, CityFormSet, TeamFormSet, HouseFormSet
from .utils import create_term, generate_term, term_start_date_from_semiannual, validate_term, \
                   check_csvfile, import_csvfile, save_file, mid_term, migrate_schedules,\
                   save_locality, save_team, save_residence
            
CSV_FILE_DIR = os.path.join('apimport', 'csvFiles')

# Create your views here.
class CreateTermView(CreateView):
    template_name = 'apimport/term_details.html'
    model = Term
    fields = []
    # model = Term
    # form_class = TermCreateForm

    # default term values--c_initweeks + c_graceweeks needs to be a multiple of 2
    c_totalweeks = 20
    c_initweeks = 0
    c_graceweeks = 2
    c_periods = (c_totalweeks - c_initweeks - c_graceweeks) / 2

    term_dates = DateForm()

    def get_context_data(self, **kwargs):
        context = super(CreateTermView, self).get_context_data(**kwargs)

        if mid_term():
            # We're in the middle term, we should only get a new CSV file for import
            context['full_input'] = False
        else:
            context['full_input'] = True
            context['season'], context['year'] = generate_term()

            semi_season = "Summer" if context['season'] == "Spring" else "Winter"

            context['start_date'] = term_start_date_from_semiannual(semi_season, context['year'])
            context['initial_weeks'] = self.c_initweeks
            context['grace_weeks'] = self.c_graceweeks
            context['periods'] = self.c_periods
            context['term_dates'] = self.term_dates
        return context

    def post(self, request, *args, **kwargs):
        if (not mid_term()):
            term_name = request.POST['termname']
            season, year = term_name.split(" ")
            
            # Store interesting variables for later -- TODO(haileyl): delete these variables
            request.session['c_initweeks'] = request.POST['initial_weeks']
            request.session['c_graceweeks'] = request.POST['grace_weeks']
            request.session['c_periods'] = request.POST['periods']

            start_date = request.POST['startdate']
            end_date = request.POST['enddate']

            start_date = datetime.strptime(start_date, "%m/%d/%Y")
            end_date = datetime.strptime(end_date, "%m/%d/%Y")

            # Refresh if bad input received
            if not validate_term(start_date, end_date, request.session['c_initweeks'], 
                request.session['c_graceweeks'], request.session['c_periods'],
                self.c_totalweeks, request):
                return self.get(request, *args, **kwargs)

            # Save term to database
            create_term(season, year, start_date, end_date)

            # Move schedules
            migrate_schedules()

        # Save out the CSV File
        # path = os.path.join("apimport", "csvFiles")
        # request.session['file_path'] = save_file(request.FILES['csvFile'], path)
        # return HttpResponseRedirect(reverse_lazy('apimport:process_csv'))
        request.session['file_path'] = save_file(request.FILES['csvFile'], CSV_FILE_DIR)

        return redirect('apimport:process_csv')

class ProcessCsvData(TemplateView):
    template_name = 'apimport/process_csv.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super(ProcessCsvData, self).get_context_data(**kwargs)

        # Check the CSV File
        localities, teams, residences = check_csvfile(self.request.session['file_path'])

        if localities or teams or residences:
            initial_locality = []
            for locality in localities:
                initial_locality.append({'name' : locality})
            context['cityformset'] = CityFormSet(initial=initial_locality, prefix='locality')

            initial_team = []
            for team in teams:
                initial_team.append({'code' : team})
            context['teamformset'] = TeamFormSet(initial=initial_team, prefix='team')

            initial_residence = []
            for residence in residences:
                initial_residence.append({'name' : residence})
            context['houseformset'] = HouseFormSet(initial=initial_residence, prefix='house')
            context['import_complete'] = False
        else: 
            import_csvfile(self.request.session['file_path'])
            context['import_complete'] = True

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

def save_data(request):
    if request.is_ajax():
        save_type = request.POST['type']
        if save_type == 'locality':
            save_locality(request.POST['city_name'], 
                          request.POST['state_id'], 
                          request.POST['country_code'])
        elif save_type == 'team':
            save_team(request.POST['team_name'], 
                      request.POST['team_code'], 
                      request.POST['team_type'], 
                      request.POST['team_locality'])
        elif save_type == 'house':
            save_residence(request.POST['house_name'],
                           request.POST['house_gender'],
                           request.POST['house_address'],
                           request.POST['house_city'],
                           request.POST['house_zip'])
    response = {'Todo(apimport2)' : 'Check failure Not an ajax call'}
    return HttpResponse(json.dumps(response), content_type="application/json")

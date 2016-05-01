import csv
from datetime import date, datetime, time, timedelta
import requests
import json
from urllib import urlencode

from django.conf import settings # for access to MEDIA_ROOT
from django.contrib import messages

from accounts.models import Trainee, User
from aputils.models import Address, City, Country
from houses.models import House
from localities.models import Locality
from teams.models import Team
from terms.models import Term

def date_for_day_of_week(date, day):
    """ returns the date of the specified day in the week identifid by date.
        For example, if date 4/9/2016 (Saturday) and 0 (Monday) are passed in,
        4/4/2016 will be returned. """
    return datetime.combine(date + timedelta(days=day-date.weekday()), time(0,0))

def term_start_date_from_semiannual(season, year):
    """ This returns the best-guess term start date for the given semi-annual.
        Input should follow the form of ("Winter"/"Summer", year) """
    if season == "Winter":
        seed_date = datetime(year, 12, 25)
    else:
        seed_date = datetime(year, 7, 4)

    # Make it a Monday
    seed_date = date_for_day_of_week(seed_date, 0)

    # return date of 19 weeks previous-- one week for semi-annual
    return datetime.combine(seed_date + timedelta(weeks=-19, days=0), time(0,0)).date()

def next_term_start_date(date):
    """ returns the next possible start term date (best guess)"""

    # Not really worth it to be smart here--just start in Spring of this year and keep 
    # going until we have a workable date.
    season = "Summer"
    year = date.year

    while True:
        start_date = term_start_date_from_semiannual(season, year)

        # give a week lee-way in case we guessed the wrong semi-annual week
        if (start_date + timedelta(7)) > date:
            return start_date

        # increment semiannual
        if season == "Summer":
            season = "Winter"
        else:
            season = "Summer"
            year = year + 1

def previous_term():
    current_term = Term.current_term()
    if current_term != None:
        return current_term.season, current_term.year

    return None, None

def generate_term():
    season, year = previous_term()

    if season == "Fall":
        season = "Spring"
        year = year + 1
    elif season == "Spring":
        season = "Fall"
    else:
        # No term found, use today's date to identify what term we are hoping to create
        today = datetime.now().date()
        start_date = next_term_start_date(today)
        if start_date.month <= 4:  # month chosen semi-arbitrarily
            return "Spring", start_date.year
        else:
            return "Fall", start_date.year

    return (season, year)

def create_term(season, year, start_date, end_date):
    term = Term()

    term.season = season
    term.year = year
    term.start = start_date
    term.end = end_date
    term.save() 
    Term.set_current_term(term)

def validate_term(start, end, c_init, c_grace, c_periods, c_totalweeks, request):
    """ Validates the provided information.  Returns true/false based
        on the validity of the data """

    success = True

    # Start needs to be a Monday and end needs to be a Sunday
    if start.weekday() != 0:
        messages.add_message(request, messages.ERROR, 
            'Term start date needs to be a Monday.')
        success = False

    if end.weekday() != 6:
        messages.add_message(request, messages.ERROR, 
            'Term end date needs to be a Lord\'s Day.')
        success = False

    if (end - start).days != (7 * c_totalweeks - 1):
        messages.add_message(request, messages.ERROR, 
            'Term length does not match requested number of weeks (' + str(c_totalweeks) + ').')
        success = False

    if (int(c_init) + int(c_grace) + int(c_periods) * 2) != c_totalweeks:
        messages.add_message(request, messages.ERROR,
            'Total number of weeks incorrect.  Total number of weeks should be: ' + str(c_totalweeks) +'.')
        success = False

    return success

def save_file(f, path):
    """ Saves file with the same filename at the given path relative to the media folder """
    full_path =  settings.MEDIA_ROOT + '\\' + path + f.name
    with open(full_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return full_path

def check_sending_locality(locality):
    if Locality.objects.filter(city__name=locality).exists():
        return True
    return False

def check_team(team):
    if Team.objects.filter(code=team).exists():
        return True
    return False

def check_residence(residence):
    if residence == 'COMMUTER':
        return True
    if House.objects.filter(name=residence).exists():
        return True
    return False

def check_office_id(id):
    # TODO: Eventually, we probably want to sanity check that the first name hasn't changed.
    # Perhaps other fields also need to be checked.
    pass

def fake_creation(localities, teams, residences):
    """ Temporarily force create all new objects in the list in a non-correct way """
    country = Country.objects.get(code='US')
    for locality in localities:
        city = City(name=locality, country=country)
        city.save()
        city = City.objects.get(name=locality)
        locality = Locality(city=city)
        locality.save()

    locality = Locality.objects.get(city__name='Anaheim')
    for team in teams:
        team = Team(name=team, code=team, type='YP', locality=locality)
        team.save()

    for residence in residences:
        address = Address(address1=residence, city=locality.city, zip_code='92804')
        address.save()
        address = Address.objects.get(address1=residence)
        house = House(name=residence, address=address, gender='B')
        house.save()


def check_csvfile(file_path):
    """ Does the necessary verification of the csvfile, returns lists of potentially new
        objects that require further processing before the csv file can be imported """

    # new entries
    localities = []
    teams = []
    residences = []

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # sendingLocality, teamID, residenceID, officeID
            if (not check_sending_locality(row['sendingLocality'])) \
                and (not row['sendingLocality'] in localities):
                localities.append(row['sendingLocality'])

            if (not check_team(row['teamID'])) \
                and (not row['teamID'] in teams):
                teams.append(row['teamID'])

            if (not check_residence(row['residenceID'])) \
                and (not row['residenceID'] in residences):
                residences.append(row['residenceID'])
        
    # fake_creation(localities, teams, residences)

    return localities, teams, residences


def import_address(row, trainee):
    ddr = row['city'] + ", " + row['state'] + ", " + row['country']

    # Key used is related to haileyl's github account
    args = {'text' : full_addr,
            'api_key' : 'search-G5ETZ3Y'}
    url = 'http://search.mapzen.com/v1/search?' + urlencode(args)

    r = requests.get(url)
    r_json = r.json()
    confidence = 0
    best = None
    for item in r_json['features']:
        if item['properties']['confidence'] > confidence:
            best = item['properties']
            confidence = best['confidence']
    
    if best != None:
        if best['country'] == "United States":
            out =  full_addr + " | " + best['name'] + ", " + best['region_a'] + ", " + best['country']
        else:
            out =  full_addr + " | " + best['name'] + ", " + best['country']
        print out.encode('unicode-escape')
    # TODO: actually import the address 

def import_row(row):
    # First create user
    try:
        user = User.objects.get(email=row['email'])
    except User.DoesNotExist:
        user = User(email=row['email'])

    user.firstname = row['stName']
    user.lastname = row['lastName']
    user.middlename = row['middleName']
    user.nickname = row['nickName']
    user.maidenname = row['maidenName']

    user.gender = row['gender']
    user.date_of_birth = datetime.strptime(row['birthDate'],  "%m/%d/%Y %H:%M")
    user.phone = row['cellPhone']
    user.is_active = True

    user.save()

    return

    try:
        trainee = Trainee.objects.get(office_id=row['officeID'])
    except Trainee.DoesNotExist:
        trainee = Trainee(office_id=row['officeID'])



    if row['residenceID'] == 'COMMUTER':
        trainee.type = 'C'
    else:
        trainee.type = 'R'

    #trainee.term = Term.current_term()
    #trainee.date_begin = trainee.term.start

    # TA
    # mentor

    # locality
    try: 
        locality = Locality.objects.filter(city__name=row['sendingLocality']).exists()
    except:
        print "Unable to set locality for trainee: " + row['stName'] + " " + row['lastName']

    try:
        team = Team.objects.get(code=row['teamID'])
        trainee.team = team
    except:
        print "Unable to set team for trainee: " + row['stName'] + " " + row['lastName']

    if row['residenceID'] != 'COMMUTER':
        try:
            residence = House.objects.get(name=row['residenceID'])
            trainee.residence = residence
        except:
            print "Unable to set house for trainee: " + row['stName'] + " " + row['lastName']

    # bunk

    trainee.married = row['maritalStatus'] == "Couple"

    # spouse -- where do we get this information from?
    # address
    import_address(row, trainee)

    trainee.self_attendance = row['termsCompleted'] >= 2
    #trainee.email = row['email']

#    trainee.save()

def import_csvfile(file_path):
    # sanity check
    localities, teams, residences = check_csvfile(file_path)
    if localities or teams or residences:
        return False

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            import_row(row)

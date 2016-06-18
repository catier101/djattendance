import csv
from datetime import date, datetime, time, timedelta
import requests
import json
import os
from urllib import urlencode


from django.conf import settings # for access to MEDIA_ROOT
from django.contrib import messages
from django_countries import countries

from accounts.models import Trainee, TrainingAssistant, User, UserMeta
from aputils.models import Address, City, State, Vehicle
from houses.models import House
from localities.models import Locality
from teams.models import Team
from terms.models import Term
from schedules.models import Schedule

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

def deactivate_user(user):
    if user.type != 'T':
        # There might be other things we need to deactivate as well.  Our other option here
        # is to, in all of these places, also filter on active=True.  There's at least
        # one place already that doesn't do this, though.
        user.is_active = False
        user.team = None
        user.house = None
        user.save()

def deactivate_previous_term():
    # Mark all trainees as inactive
    # TODO (import2): Probably should consider doing this only on trainees related to the 
    # current term.  Though I kind of prefer doing this on all trainees, so we can start
    # every term in a very clean state.
    for u in User.objects.all():
        deactivate_user(u)

        # TODO(import2): are there permissions that we care to deactivate here?  Team 
        # monitors maybe?  HCs should be taken care of on a trainee by trainee basis 
        # as they are reactivated.


def create_term(season, year, start_date, end_date):
    """ Creates a new term after deactivating the previous term.  This function
        DOES NOT CHECK to see if the data you're passing in is good or not.  
        MAKE THE PROPER CHECKS FIRST."""

    deactivate_previous_term()

    try:
        term = Term.objects.get(season=season, year=year)
        term.start = start_date
        term.end = end_date
        term.save()
    except Term.DoesNotExist:
        term = Term(season=season, year=year, start=start_date, end=end_date)
        term.save()

    Term.set_current_term(term)

def mid_term():
    """ Returns true if we are still in the current term or if the current term hasn't yet
        started yet """
    term = Term.current_term()
    if term != None and date.today() < term.end:
        return True

    return False

def validate_term(start, end, c_init, c_grace, c_periods, c_totalweeks, request):
    """ Validates the provided information.  Returns true/false based
        on the validity of the data """
    is_success = True

    # Start needs to be a Monday and end needs to be a Sunday
    if start.weekday() != 0:
        messages.add_message(request, messages.ERROR, 
            'Term start date needs to be a Monday.')
        is_success = False

    if end.weekday() != 6:
        messages.add_message(request, messages.ERROR, 
            'Term end date needs to be a Lord\'s Day.')
        is_success = False

    if (end - start).days != (7 * c_totalweeks - 1):
        messages.add_message(request, messages.ERROR, 
            'Term length does not match requested number of weeks (' + str(c_totalweeks) + ').')
        is_success = False

    if (int(c_init) + int(c_grace) + int(c_periods) * 2) != c_totalweeks:
        messages.add_message(request, messages.ERROR,
            'Total number of weeks incorrect.  Total number of weeks should be: ' + str(c_totalweeks) +'.')
        is_success = False

    # Is the current term finished yet?
    if mid_term():
        messages.add_message(request, messages.ERROR,
            'Cannot start a new term before previous term has ended!')
        is_success = False

    return is_success

def save_file(f, path):
    """ Saves file with the same filename at the given path relative to the media folder """
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    full_path = os.path.join(file_path, f.name)

    dir = os.path.dirname(full_path)
    if not os.path.isdir(dir):
        os.makedirs(dir)

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

def save_locality(city_name, state_id, country_code):
    if country_code == 'US' and state_id:
        state = State.objects.get(id=state_id)
    else:
        state = None

    city, created = City.objects.get_or_create(name=city_name, state=state, country=country_code)
    locality, created = Locality.objects.get_or_create(city=city)

def save_team(name, code, type, locality):
    team, created = Team.objects.get_or_create(name=name, 
                                               code=code, 
                                               locality_id=locality, 
                                               type=type)

def save_residence(name, gender, address, city, zip):
    address, created = Address.objects.get_or_create(address1=address, city_id=city, zip_code = zip)
    house, created = House.objects.get_or_create(name=name, address=address, gender=gender)

def check_csvfile(file_path):
    """ Does the necessary verification of the csvfile, returns lists of potentially new
        objects that require further processing before the csv file can be imported """

    fake = False

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

                if fake:
                    save_locality(row['sendingLocality'], 1, 'US')
                else:
                    localities.append(row['sendingLocality'])

            if (not check_team(row['teamID'])) \
                and (not row['teamID'] in teams):
                if fake:
                    save_team("Team", row['teamID'], 1, 'CAMPUS')
                else:
                    teams.append(row['teamID'])

            if (not check_residence(row['residenceID'])) \
                and (not row['residenceID'] in residences):
                if fake:
                    save_residence(row['residenceID'], 2, 'B')
                else:
                    residences.append(row['residenceID'])
    return localities, teams, residences

def countrycode_from_alpha3(code3):
    """Converts from a three-letter country code to a 2-letter country code if such a 
       matching exists. """
    for country in countries:
        if countries.alpha3(country[0]) == code3:
            return country[0]

    return None

def import_address(address, city, state, zip, country):
    try:
        address_obj = Address.objects.get(address1=address)
        return address_obj
    except Address.DoesNotExist:
        pass

    addr = city + ", " + state + ", " + country
    # Key used is related to haileyl's github account
    args = {'text' : addr,
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

    if best == None:
        return

    code = best['country_a']
    if len(code) == 3:
        code = countrycode_from_alpha3(code)

    city_obj, created = City.objects.get_or_create(name=best['name'], country=code)
    if created and code == "US":
        state_obj = None
        if best['region'] == "Puerto Rico":
            state_obj, created = State.objects.get_or_create(name="PR")
        elif best['region'] == "District of Columbia":
            state_obj, created = State.objects.get_or_create(name="DC")
        elif 'region_a' in best:
            state_obj, created = State.objects.get_or_create(name=best['region_a'])

        if state_obj != None:
            city_obj.state = state_obj
            city_obj.save()

    try:
        zip_int = int(zip)
    except ValueError:
        zip_int = None

    address_obj, created = Address.objects.get_or_create(
        address1=address,
        city=city_obj,
        zip_code=zip_int)

    return address_obj

def gospel_code(choice):
    if choice.lower() == "campus":
        return "CP"
    elif choice.lower() == "yp":
        return "YP"
    elif choice.lower() == "children":
        return "CH"
    elif choice.lower() == "community":
        return "CM"
    elif choice.lower() == "i-dcp":
        return "ID"

    return None

def import_row(row):
    """ Creates or updates a user based on the given row.  Matches user first by office_id
        and then by email address """
    # First create/update user -- Assume Csv is correct, all information gets overriden
    try:
        user = User.objects.get(office_id=row['officeID'])
        user.email = row['email']
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=row['email'])
            user.office_id = row['officeID']
        except User.DoesNotExist:
            user = User(email=row['email'], office_id=row['officeID'])

    user.save()

    if row['residenceID'] == 'COMMUTER':
        user.type = 'C'
    else:
        user.type = 'R'

    user.firstname = row['stName']
    user.lastname = row['lastName']
    user.middlename = row['middleName']
    user.nickname = row['nickName']

    user.gender = row['gender']
    user.date_of_birth = datetime.strptime(row['birthDate'],  "%m/%d/%Y %H:%M")
    user.is_active = True

    term = Term.current_term()
    user.terms_attended.add(term)

    user.current_term = int(row['termsCompleted']) + 1
    
    if user.date_begin == None:
        user.date_begin = term.start
    user.date_end = term.end

    #TA
    #Mentor

    try: 
        # TODO: This needs to be done better, once we get more information about localities
        locality = Locality.objects.filter(city__name=row['sendingLocality'])[0]
    except:
        print "Unable to set locality for trainee: " + row['stName'] + " " + row['lastName']

    try:
        team = Team.objects.get(code=row['teamID'])
        user.team = team
    except:
        print "Unable to set team for trainee: " + row['stName'] + " " + row['lastName']

    # TODO (import2): permissions
    user.is_hc = row['HouseCoor'] == "TRUE"

    if row['residenceID'] != 'COMMUTER':
        try:
            residence = House.objects.get(name=row['residenceID'])
            user.house = residence
        except:
            print "Unable to set house for trainee: " + row['stName'] + " " + row['lastName']

    user.self_attendance = user.current_term > 2
    user.save()

    # META
    try:
        meta = user.meta
    except UserMeta.DoesNotExist:
        meta = UserMeta(user=user)
    meta.phone = row['cellPhone']
    meta.home_phone = row['homePhone']
    meta.work_phone = row['workPhone']

    meta.maidenName = row['maidenName']
    meta.is_married = row['maritalStatus'] == "Couple"
    meta.is_couple = row['couples'] == "1"

    meta.address = import_address(row['address'], 
                                  row['city'], 
                                  row['state'], 
                                  row['zip'], 
                                  row['country'])

    meta.college = row['college']
    meta.major = row['major']
    meta.degree = row['degree']

    meta.emergency_name = row['emergencyContact']
    meta.emergency_address = row['emergencyAddress']
    meta.emergency_phone = row['emergencyPhoneNumber']
    meta.emergency_phone2 = row['emergencyPhoneNumber2']

    meta.gospel_pref1 = gospel_code(row['gospelPreference1'])
    meta.gospel_pref2 = gospel_code(row['gospelPreference2'])

    meta.readOT = row['readOldTestament'] == "TRUE"
    meta.readNT = row['readNewTestament'] == "TRUE"

    meta.save()

    if row['vehicleYesNo'] == "FALSE":
        user.vehicles.all().delete()
    else:
        Vehicle.objects.get_or_create(color=row['vehicleColor'], 
                                      model=row['vehicleModel'], 
                                      license_plate=row['vehicleLicense'],
                                      capacity=row['vehicleCapacity'],
                                      user=user)


def import_csvfile(file_path):
    # sanity check
    localities, teams, residences = check_csvfile(file_path)
    if localities or teams or residences:
        return False

    print "Beginning import..."
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            import_row(row)

    term = Term.current_term()
    schedules = Schedule.objects.filter(term=term)

    print schedules
    for schedule in schedules:
        schedule.assign_trainees_to_schedule()

def term_before(term):
    if not term:
        return None

    season = "Spring" if term.season == "Fall" else "Fall"
    year = term.year if term.season == "Fall" else term.year - 1

    try:
        term_minus = Term.objects.get(season=season, year=year)
    except Term.DoesNotExist:
        term_minus = None

    return term_minus

def migrate_schedule(schedule):
    if schedule == None:
        return

    schedule2 = schedule
    schedule2.pk = None
    schedule2.date_created = datetime.now()
    schedule2.is_locked = False
    schedule2.term = Term.current_term()
    schedule2.save()
    schedule2.events.add(*schedule.events.all())
    schedule2.save()
    return schedule2

def migrate_schedules():
    term = Term.current_term()
    term_minus_one = term_before(term)
    term_minus_two = term_before(term_minus_one)

    schedule_set = []

    schedules = Schedule.objects.filter(term=term_minus_one, import_to_next_term=True, season="All")
    schedule_set.extend(schedules)

    schedules = Schedule.objects.filter(term=term_minus_two, import_to_next_term=True, season=term.season)
    schedule_set.extend(schedules)

    for schedule in schedule_set:
        s_new = migrate_schedule(schedule)
from django.core.management.base import BaseCommand
from accounts.models import User
from terms.models import Term

class Command(BaseCommand):
    # to use: python ap/manage.py populate_users --settings=ap.settings.dev
    def _create_users(self):
        # change the array below to get different trainees
        trainees = ['Carlos Ospina','Rodney Rodriguez','Daniel Kim','Cephas Chen','Jared Hermelin','Samuel Sun','Kevin Ger','John Ferrante','John Gim','Keaton Robinson','Sam Bae','Allen Liu','David Jung','Chris Shyy','Abraham Romero','Peter Pensuwan','Isaac Choo','Jacob Chen','Samuel Oh','Jonathan Tey','David Tien','Joseph Duque','Joon Jo','Jarrod Frankum','Leo Medina','Tony Damian','Philip Lam','Tim Higashi','Dinglu Chen','Martinez Hugo Jr.','Jean Jeong','Andy Li','Andrew Sun','WeiLung Ho','David Li','Dustin Davis','Andrew Dina','Samuel Chiu','John Ku','Ben Wang','Samuel Lee','Leonard Lan','Terry Hung','Samuel Chai','Joseph Hur','Joshua Chang','Joseph Meng','Kyle Seay','Julian Arango','Josh Shen','David Miyamoto','Ryan Danek','Joshua Obidah','Samuel Yu','Jerry Alvarez','Joe Zhou','Tommy Giordano','Ugo Ibe','Ian Wolf','Jeffrey Chan','Alfred Meng','Seth Packwood','Matthew Nichols','Osric Jen','Samuel Yusuf','Eric Chong','David Tai','Juanito Novikov','Andreas Andreas','Michael Ng','Vince Pau','Ben Schulz','Paul Sutton','Victor Shih','Caven Gao','Daniel Teng','Peter Cheng','Ruiyu Wu','Xavier Christian','Nelson Liu','Brian Lu','Travis Rigsby','Travis Hall']
        for trainee in trainees:
            print trainee
            email = '.'.join(trainee.lower().split(' ')) + "@gmail.com"
            firstname = trainee.split(' ')[0]
            lastname = trainee.split(' ')[1]
            gender = 'B'
            password = 'ap'
            date_of_birth = '1993-11-13'
            u = User(email=email, firstname=firstname, lastname=lastname, gender=gender, password=password, type='R', date_of_birth=date_of_birth)
            u.save()

        print 'done'

    def handle(self, *args, **options):
        self._create_users()
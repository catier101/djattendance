from django.db import models

from accounts.models import Profile
from houses.models import House

""" absent_trainee_roster models.py
The absent trainee roster module takes care of generating daily absent trainee rosters
from HC imported forms.

ABSENTEE 
-represents each trainee as an absentee

ROSTERMANAGER 
-initializes each newly created roster with the list of houses that need to submit their absent trainee form

ROSTER 
-compiles all the absent trainee forms submitted on a given date

ENTRY 
-form submitted by the house coordinators to be compiled and generated as the roster

"""

class Absentee(Profile):
	
	def __unicode__(self):
		return self.account.get_full_name()
	
	def _trainee_name(self):
		return self.account.get_full_name()
	
	def _trainee_house(self):
		return self.account.trainee.house
	
	def _trainee_term(self):
		return self.account.trainee.current_term
	
	name = property(_trainee_name)
	house = property(_trainee_house)
	term = property(_trainee_term)


class RosterManager(models.Manager):
	# when roster is created in admin, admin calls RosterAdmin.save_related()
	# to add the unreported houses.
	def create_roster(self, date):
		roster = self.create(date=date)
		roster.save() # have to save before adding many-to-many relationship
		# initialize with all houses unreported (remove houses from list when hc submits form).
		for house in House.objects.all(): 
			roster.unreported_houses.add(house)
		roster.save()
		return roster


class Roster(models.Model):
	date = models.DateField(primary_key=True)
	
	objects = RosterManager()
	unreported_houses = models.ManyToManyField(House, related_name= 'rosters', blank=True, null=True)

	def __unicode__(self):
		return self.date.strftime("%m/%d/%Y") + "roster"


class Entry(models.Model):
	
	ABSENT_REASONS = (
        ('C', 'Conference'), 
        ('SI', 'Sick'),
        ('SE', 'Service'),
        ('O', 'Other'),
        ('T', 'Out of Town'),
        ('F', 'Fatigue'),
    )
	
	roster = models.ForeignKey(Roster)
	absentee = models.ForeignKey(Absentee)
	reason = models.CharField(max_length=2, choices=ABSENT_REASONS)
	coming_to_class = models.BooleanField(default=False)
	comments = models.CharField(max_length=250, blank=True)

	class Meta:
		verbose_name_plural = 'entries'

	def __unicode__(self):
		return self.absentee.name

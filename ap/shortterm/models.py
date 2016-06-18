from django.db import models
from accounts.models import User, Trainee
from localilties.models import Locality
from houses.models import House, Bunk
from terms.models import Term

""" shortterm models.py 
This class represents short-term trainees.
"""

class ShortTermTrainee(User):

    visits = models.ManyToManyField('Visit')

class Visit(models.Model):
    """ a single short-term visit """

    application = models.ForeignKey('Application')

    term = models.ForeignKey(Term)

    arrivalDate = models.DateField()

    departureDate = models.DateField()

    mentor = models.ForeignKey(Trainee)

    house = models.ForeignKey(House)

    bunk = models.ForeignKey(Bunk)

class Application(models.Model):
    """ an application to short term at the FTTA """

    locality = models.ForeignKey(Locality)

    recommendation = models.TextField()

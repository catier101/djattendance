from django.db import models
from accounts.models import User
from houses.models import House, Bunk

"""  hospitality models.py 
This module takes care of all the logistics of LSM hospitality.

"""

class HospitalityGuest(User):

    visits = models.ManyToManyField('Visit')

class Visit(models.Model):
    """ a single stay with LSM hospitality """

    arrivalDate = models.DateField()

    departureDate = models.DateField()
    
    arrivalDate = models.DateField()

    departureDate = models.DateField()

    house = models.ForeignKey(House)

    bunk = models.ForeignKey(Bunk)

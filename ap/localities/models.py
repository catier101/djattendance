from django.db import models

from aputils.models import City
from django_countries.fields import CountryField

""" LOCALITIES models.py

The Localities module is a utility module underlying other apps. In particular,
both trainees are related to localities (as being sent from), and teams are
related to localities (as serving in).

Data Models:
    - Locality: a local church
"""


class Locality(models.Model):

    city = models.ForeignKey(City)
    #country = CountryField()

    def __unicode__(self):
        return self.city.name + ", " + str(self.city.state)

    class Meta:
        verbose_name_plural = 'localities'

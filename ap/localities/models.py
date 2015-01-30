from django.db import models

from aputils.models import City

""" LOCALITIES models.py

The Localities module is a utility module underlying other apps. In particular,
both trainees are related to localities (as being sent from), and teams are
related to localities (as serving in).

Data Models:
    - Locality: a local church
"""


class Locality(models.Model):

    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.city

    class Meta:
        verbose_name_plural = 'localities'

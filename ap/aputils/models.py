from django.db import models

from django_countries.fields import CountryField

""" APUTILS models.py

The APUTILS model handles various miscellaneous data models that will be used
widely across other files.

Data Models:
    - Country: A standard country, used in cities.
    - City: A standard city anywhere in the world, used in localities and
    addresses
    - Address: A standard US address used for training residences, emergency
    contact information, and other things
    - Vehicle: Represents vehicles owned by trainees
    - EmergencyInfo: Emergency contact info for a trainee, used in accounts
"""
class State(models.Model):

    STATES = (
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'),
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'),
        ('PR', 'Puerto Rico'),
    )
    
    name = models.CharField(max_length=2, blank=True, choices=STATES, unique=True)

    def __unicode__(self):
        return self.get_name_display()


class City(models.Model):

    # the name of the city
    name = models.CharField(max_length=50)

    # optional for non-US cities
    state = models.ForeignKey(State, blank=True, null=True)

    # Country foreign key
    country = CountryField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class Address(models.Model):

    # line 1 of the address field
    address1 = models.CharField(max_length=150)

    # line 2 of the address field
    address2 = models.CharField(max_length=150, blank=True)

    # City foreign key
    city = models.ForeignKey(City)

    zip_code = models.PositiveIntegerField(null=True, blank=True)

    # optional four-digit zip code extension
    zip4 = models.PositiveSmallIntegerField(null=True, blank=True)

    # optional details field
    details = models.CharField(max_length=150, null=True, blank=True)

    def __unicode__(self):
        adr1, adr2 = self.address1, self.address2
        # don't include the newline if address2 is empty
        return adr1 + '\n' + adr2 if adr2 else adr1

    class Meta:
        verbose_name_plural = "addresses"


class HomeAddress(Address):
    trainee = models.ForeignKey('accounts.Trainee')


class Vehicle(models.Model):

    color = models.CharField(max_length=20, blank=True, null=True)

    # e.g. "Honda", "Toyota"
    make = models.CharField(max_length=30, blank=True, null=True)

    # e.g. "Accord", "Camry"
    model = models.CharField(max_length=30, blank=True, null=True)

    year = models.PositiveSmallIntegerField(blank=True, null=True)

    license_plate = models.CharField(max_length=25, blank=True, null=True)

    state = models.CharField(max_length=20, blank=True, null=True)

    capacity = models.PositiveSmallIntegerField()

    user = models.ForeignKey('accounts.User', related_name='vehicles', blank=True, null=True)

    def __unicode__(self):
        return self.color + ' ' + self.make + ' ' + self.model


class EmergencyInfo(models.Model):

    name = models.CharField(max_length=255)

    #contact's relation to the trainee.
    relation = models.CharField(max_length=30)

    phone = models.CharField(max_length=15)

    phone2 = models.CharField(max_length=15, blank=True, null=True)

    address = models.ForeignKey(Address)
    
    trainee = models.OneToOneField('accounts.Trainee', blank=True, null=True)

    def __unicode__(self):
        return self.name + '(' + self.relation + ')'


class QueryFilter(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    # Dictionary of all filters applied to query
    query = models.TextField()

    def __unicode__(self):
        return self.name
        q = eval(self.query)
        return '%s - %s' % (self.name, '(' + ','.join(['%s=%s' %(k, v) for k, v in q.items()]) + ')')

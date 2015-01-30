from django.db import models

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


class Country(models.Model):

    # the name of the country
    name = models.CharField(max_length=50)

    # e.g. "USA", "JPN"
    code = models.CharField(max_length=3)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"


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
    )
    
    name = models.CharField(max_length=2, blank=True, choices=STATES)


class City(models.Model):

    # the name of the city
    name = models.CharField(max_length=50)

    # optional for non-US cities
    state = models.ForeignKey(State, blank=True, null=True)

    # Country foreign key
    country = models.ForeignKey(Country)

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

    zip_code = models.PositiveIntegerField()

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

    color = models.CharField(max_length=20)

    # e.g. "Honda", "Toyota"
    make = models.CharField(max_length=30)

    # e.g. "Accord", "Camry"
    model = models.CharField(max_length=30)

    year = models.PositiveSmallIntegerField()

    license_plate = models.CharField(max_length=10)

    state = models.CharField(max_length=20)

    capacity = models.PositiveSmallIntegerField()

    trainee = models.ForeignKey('accounts.Trainee', blank=True, null=True)

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

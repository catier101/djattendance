from django.db import models
from aputils.models import Address

""" HOUSES models.py

This houses module is a utility model that define training housing.

Data Models:
    - House: a training house
    - Room: a room inside a training house (any type)
    - Bunk: a bunk (either lower of upper) in a given house
"""


class House(models.Model):

    GENDER = (
        ('B', 'Brother'),
        ('S', 'Sister'),
        ('C', 'Couple')
    )

    # the common name for the house, e.g. 1329 Amberwick, 2102 Grace
    name = models.CharField(max_length=50)

    # the house's address (defined in the utils class)
    address = models.ForeignKey(Address)

    # a house can designated for either brothers, sisters, or a couple
    gender = models.CharField(max_length=1, choices=GENDER)

    # whether this house is actively used by the training
    used = models.BooleanField()
    
    #returns a query set of the empty bunks for this house
    def empty_bunk_count(self,position_list=[]):
        if len(position_list)==0:
            return Bunk.objects.filter(room__house=self).exclude(trainee__active=True).count()
        return Bunk.objects.filter(room__house=self,position__in=position_list).exclude(trainee__active=True).count()

    def __unicode__(self):
        return u' %s' % (self.name)


class Room(models.Model):

    ROOM_TYPES = (
        ('LIV', 'Living Room'),
        ('BED', 'Bedroom'),
        ('KIT', 'Kitchen'),
        ('BATH', 'Bathroom'),
        ('GAR', 'Garage'),
        ('PAT', 'Patio'),
    )

    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    type = models.CharField(max_length=4, choices=ROOM_TYPES)

    # optional field for specifying the physical size of the room
    # useful mainly for hospitality/short-term assignments
    size = models.CharField(max_length=1, choices=SIZES, null=True, blank=True)

    # refers to number of beds
    capacity = models.SmallIntegerField(default=0)  # 0 if room is not a bedroom

    house = models.ForeignKey(House)

    floor = models.SmallIntegerField(default=1)

    def __unicode__(self):
        return "("+str(self.id)+") "+self.house.name + " " + self.type


class Bunk(models.Model):

    POSITION = (
        ('B', 'Bottom'),
        ('T', 'Top'),
        ('L', 'Queen-Left'),  # for couples
        ('R', 'Queen-Right'), 
        ('S', 'Single')
    )

    LENGTH = (
        ('R', 'Regular'),
        ('L', 'Long')
    )

    FRAME_TYPES = (
        ('M', 'Metal'),
        ('C', 'Cot'),
        ('H', 'Wood Honey'),
        ('W', 'Wood Walnut'),
        ('WC', 'Wood Walnut Crown'),
        ('O', 'Wood Oak'),
        ('LV', 'Wood Light Vintage'),
    )

    # the bunk's number
    number = models.SmallIntegerField()

    # whether this is a top or bottom bunk
    position = models.CharField(max_length=1, choices=POSITION)

    # which bunk this bunk is linked to, if any
    link = models.OneToOneField('Bunk', null=True, blank=True)

    # which room this bunk is in
    room = models.ForeignKey(Room)
    
    length = models.CharField(max_length=1, choices=LENGTH, default='R')
    
    # type of bed frame
    frame = models.CharField(max_length=2, choices=FRAME_TYPES, null=True, blank=True)
    
    # type of mattress
    mattress = models.CharField(max_length=50, null=True, blank=True)

    # whether bunk has a guardrail
    guardrail = models.NullBooleanField(blank=True)
    
    # whether bunk has a ladder
    ladder = models.NullBooleanField(blank=True)
    
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.room.house.name + " Bunk " + str(self.number)
    

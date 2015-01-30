"""
from django.test import TestCase

from houses.models import House, Room, Bunk

class HouseTests(TestCase):

    def setUp(self):
        h = House.objects.create(
            name='Sarah', 
            address1='2119 Grace', 
            address2='Cambridge', 
            gender='S', 
            used=True
        )
        r = Room.objects.create(capacity=4, house=h)
        b = Bunk.objects.create(number=1, position='T', room=r)

    def test_address_returns_right_value(self):
        h = House.objects.get(name='Sarah')
        house_address = h.address
        con_address = h.address1 + '\n' + h.address2
        name = h.name
        self.assertEqual(name, h)
        self.assertEqual(house_address, con_address)

    def test_room_returns_right_value(self):
        h = House.objects.get(name='Sarah')
        room = Room.objects.get(house=h)
        ck_room = room.house.name + ' Room ' + str(room.pk)
        self.assertEqual(room, ck_room)

    def test_bunk_returns_right_value(self):
        h = House.objects.get(name='Sarah')
        r = Room.objects.get(house=h)
        b = Bunk.objects.get(room=r)
        ck_bunk=b.room.house.name + ' Bunk ' + str(b.number)
        self.assertEqual(b.position, 'T')
        self.assertEqual(ck_bunk, b)
"""
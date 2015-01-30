"""
from django.test import TestCase
from rooms.models import Room

class RoomsTest(TestCase):
    def setUp(self):
        r = Room.objects.create(
            code="154B", 
            name="West Side Third Heavens", 
            floor=3, 
            type="SR", 
            access="S"
        )

    def test_room_returns_right_value(self):
        r = Room.objects.get(code="154B")
        self.assertEqual(r.type, "SR")
        self.assertEqual(r.access, "S")
"""
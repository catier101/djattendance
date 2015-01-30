"""
from django.test import TestCase

from aputils.models import Address, City, Country, Vehicle

def setup_country():
    country = Country(name='Lala Land', code='LLL')
    country.save()
    return country

def setup_city():
    country = setup_country()
    city = City(
        name='Lala City',
        region='Lalalandia',
        country=country,
    )
    city.save()
    return city

def setup_address():
    city = setup_city()
    address = Address(
        address1='1234 Main St.',
        address2='P.O. Box 1234',
        city=city,
        zip_code=12345,
        zip4=1234,
        details='Insert details here.',
    )
    address.save()
    return address

def setup_vehicle():
    vehicle = Vehicle(
        color='dark blue',
        make='Toyota',
        model='Corolla',
        license_plate='1ABC234',
    )
    vehicle.save()
    return vehicle


class AddressTests(TestCase):

    def test_create_address(self):
        setup_address()

    def test_delete_address(self):
        address = setup_address()
        address.delete()

    def test_address_unicode_with_address1_and_address2(self):
        address = setup_address()
        correctValue = '1234 Main St.\nP.O. Box 1234'
        self.assertEqual(correctValue, address.__unicode__())

    def test_address_unicode_with_address1_only(self):
        address = setup_address()
        address.address2 = ''
        correct_value = '1234 Main St.'
        self.assertEqual(correct_value, address.__unicode__())


class CityTests(TestCase):

    def test_create_city(self):
        setup_city()

    def test_delete_city(self):
        city = setup_city()
        city.delete()

    def test_city_unicode(self):
        city = setup_city()
        correct_value = 'Lala City'
        self.assertEqual(correct_value, city.__unicode__())


class CountryTests(TestCase):

    def test_create_country(self):
        setup_country()

    def test_delete_country(self):
        country = setup_country()
        country.delete()

    def test_country_unicode(self):
        country = setup_country()
        correct_value = 'Lala Land'
        self.assertEqual(correct_value, country.__unicode__())


class VehicleTests(TestCase):

    def test_create_vehicle(self):
        setup_vehicle()

    def test_delete_vehicle(self):
        vehicle = setup_vehicle()
        vehicle.delete()

    def test_vehicle_unicode(self):
        vehicle = setup_vehicle()
        correct_value = 'dark blue Toyota Corolla'
        self.assertEqual(correct_value, vehicle.__unicode__())
"""

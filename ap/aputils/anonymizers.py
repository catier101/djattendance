from aputils.models import State, City, Address, HomeAddress, Vehicle, EmergencyInfo
from anonymizer import Anonymizer

class StateAnonymizer(Anonymizer):

    model = State

    attributes = [
        ('id', "SKIP"),
        ('name', "SKIP"),
    ]


class CityAnonymizer(Anonymizer):

    model = City

    attributes = [
        ('id', "SKIP"),
        ('name', "SKIP"),
        ('state_id', "SKIP"),
        # ('country_id', "SKIP"),
    ]


class AddressAnonymizer(Anonymizer):

    model = Address

    attributes = [
        ('id', "SKIP"),
        ('address1', "full_address"),
        ('address2', "similar_lorem"),
        ('city_id', "SKIP"),
        ('zip_code', "zip_code"),
        ('zip4', "SKIP"),
        ('details', "similar_lorem"),
    ]


class HomeAddressAnonymizer(Anonymizer):

    model = HomeAddress

    attributes = [
        ('id', "SKIP"),
        ('address_ptr_id', "SKIP"),
        ('address1', "full_address"),
        ('address2', "full_address"),
        ('city_id', "SKIP"),
        ('zip_code', "positive_integer"),
        ('zip4', "positive_small_integer"),
        ('details', "varchar"),
        ('trainee_id', "SKIP"),
    ]


class VehicleAnonymizer(Anonymizer):

    model = Vehicle

    attributes = [
        ('id', "SKIP"),
        ('color', "similar_lorem"),
        ('make', "company"),
        ('model', "last_name"),
        ('year', "positive_small_integer"),
        ('license_plate', "similar_lorem"),
        ('state', "state"),
        ('capacity', "positive_small_integer"),
        ('trainee_id', "SKIP"),
    ]


class EmergencyInfoAnonymizer(Anonymizer):

    model = EmergencyInfo

    attributes = [
        ('id', "SKIP"),
        ('trainee_id', "SKIP"),
        ('name', "full_name"),
        ('relation', "SKIP"),
        ('phone', "phonenumber"),
        ('phone2', "phonenumber"),
        ('address_id', "SKIP"),
    ]

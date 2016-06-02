"""
from django.test import TestCase
from services.models import Category, Service, Period


class ServiceTest(TestCase):
    def setUp(self):
        # sets up category 'cleaning', then adds service objects 'breakfastCleanup', 'vacuuming'
        cleaning = Category.objects.create(name="cleaning", description="vacuuming, lunch cleanup, etc.")
        breakfastCleanup = Service.objects.create(category=cleaning, name="Breakfast Cleanup", active=True, workload=2)
        vacuuming = Service.objects.create(category=cleaning, name="Vacuuming", active=False, workload=1)
        # creates period 'regularWeek', then addes services 'breakfastCleanup', 'vacuuming' to that period
        regularWeek = Period.objects.create(name="FTTA Regular Week", description="Regular Week",
                                            startDate="2013-06-28", endDate="2013-07-07")
        regularWeek.service.add(breakfastCleanup, vacuuming)

    def test_category_get_services(self):
        # checks if category lists all services in that category
        c = Category.objects.get(name="cleaning")

        self.assertEqual('[<Service: Vacuuming>, <Service: Breakfast Cleanup>]', str(c.getServices()))

    def test_category_attributes(self):
        # checks if properties are valid
        c = Category.objects.get(name="cleaning")
        self.assertEqual("cleaning", c.name)
        self.assertEqual("vacuuming, lunch cleanup, etc.", c.description)

    def test_delete_objects(self):
        # deletes objs and tests if they exist
        b = Service.objects.get(name="Breakfast Cleanup")
        b.delete()
        self.assertEqual("[<Service: Vacuuming>]", str(Service.objects.all()))

    def test_period_get_service(self):
        # checks if period lists all services in that period
        d = Period.objects.get(name="FTTA Regular Week")
        self.assertEqual('[<Service: Breakfast Cleanup>, <Service: Vacuuming>]', str(d.service.all()))
"""

from localities.models import Locality
import unittest
import mock

def set_up_data():
        # model1: Locality
        # notice each instance is made to cover different combinations of attribute values
        l1=Locality(city="Melbourne", province="New South Wales", country="AUS")
        # 50 letters
        l2=Locality(city="Chargoggagoggmanchauggagoggchaubunagungamaugg City", state="MA")
        l3=Locality(city="Los Angeles", state="CA", country ="USA")
        l4=Locality(city="Kitchener", state="", country = "CAN")
        l5=Locality(city="Virginia Beach", country="USA")

        return dict([('l1', l1),('l2',l2),('l3', l3),('l4',l4), ('l5',l5)])

class LocalitiesTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_models(self):
        data_dicts = set_up_data()
        self.assertTrue(Locality(data_dicts['l1']))
        self.assertTrue(Locality(data_dicts['l2']))
        self.assertTrue(Locality(data_dicts['l3']))
        self.assertTrue(Locality(data_dicts['l4']))
        self.assertTrue(Locality(data_dicts['l5']))

    def test_for_foreignkey_in_Localities_objects(self):
        pass

    def test_unicode_functions(self):
        data_dicts = set_up_data()
        self.assertEqual('Melbourne, AUS', str(data_dicts['l1']))
        self.assertEqual('Chargoggagoggmanchauggagoggchaubunagungamaugg City, MA', str(data_dicts['l2']))
        self.assertEqual('Los Angeles, CA', str(data_dicts['l3']))
        self.assertEqual('Kitchener, CAN', str(data_dicts['l4']))
        self.assertEqual('Virginia Beach, USA', str(data_dicts['l5']))

    def tearDown(self):
        pass



"""
Refer also to books/tests for unit-test example
This class is intended to also serve as example on how to mock models to maintain decoupling
Note: this unit-test is ONLY considered complete when coverage for "classes/models" = 100%
"""

from terms.models import Term
from classes.models import Class

import unittest
import mock

def set_up_data():
        # model1: Class without term, all types tested
        c1=Class(name='Experience of Christ as Life', code='ECAL',type='1YR')
        c2=Class(name='God Ordained Way', code='GOW',type='MAIN')
        c3=Class(name='New Jerusalem', code='NJ',type='2YR')

        # foreign model: Term
        # left here for comparison with mock method which does not need this line
        t= Term(current=True, season="Fall", year=2014)
        
        c4=Class(name='Character', code='CHAR',term = t, type='AFTN')
        return dict([('c1', c1),('c2',c2),('c3', c3),('c4',c4)])

class ClassesTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_models(self):
        data_dicts = set_up_data()
        self.assertTrue(Class(data_dicts['c1']))
        self.assertTrue(Class(data_dicts['c2']))
        self.assertTrue(Class(data_dicts['c3']))
        self.assertTrue(Class(data_dicts['c4']))

    def test_class_type_choices(self):
        data_dicts = set_up_data()
        self.assertEqual(data_dicts['c1'].type, "1YR")
        self.assertEqual(data_dicts['c2'].type, "MAIN")
        self.assertEqual(data_dicts['c3'].type, "2YR")
        self.assertEqual(data_dicts['c4'].type, "AFTN")

    # don't forget to test the fields that are not explicitly declared in the data set_up
    # this test is left here for comparison with mock test below it for comparison sake
    # purpose of this test: validating the foreign key import is successful
    # either test can be used, each for its own purpose
    def test_for_foreignkey_in_Class_objects(self):
        data_dicts = set_up_data()
        self.assertEqual(data_dicts['c4'].term.current, True)
        self.assertEqual(data_dicts['c4'].term.season, "Fall")
        self.assertEqual(data_dicts['c4'].term.year, 2014)
        self.assertEqual(str(data_dicts['c4'].term), "Fall 2014")
        self.assertIsNone(data_dicts['c4'].term.start)
        self.assertIsNone(data_dicts['c4'].term.end) 

    # when using mock for term model, so any changes to Term module will not interfere this test
    # this is more ideal because unit test for class should not test "Term"
    # purpose of this test: validating the foreign key model integrity
    # notice the mock does not need set_up_data return value, thus making it cleaner
    def test_term_str(self): 
        mock_instance = mock.Mock(spec=Term) 
        mock_instance.season = "Fall" 
        mock_instance.year = 2014
        self.assertEqual(Term._name(mock_instance), "Fall 2014")
        self.assertEqual(Term._code(mock_instance), "Fa14")

    def test_unicode_functions(self):
        data_dicts = set_up_data()
        self.assertEqual('Experience of Christ as Life', str(data_dicts['c1']))
        self.assertEqual('God Ordained Way', str(data_dicts['c2']))
        self.assertEqual('New Jerusalem', str(data_dicts['c3']))
        self.assertEqual('Character', str(data_dicts['c4']))

    def tearDown(self):
        pass


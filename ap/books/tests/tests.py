"""
This file shows example how to avoid database writes during testing.
It also serves as example to go through the models one by one and making sure
all boundary cases are taken care of. Look at the setup commentaries to see systematically 
how the tests are thought for.
Pay attention to:
1. set_up_data before the class definition
2. test_names definitions inside of the class
3. coverage scope of each test definition
4. how to retrieve created data globally from data generator outside the class
And don't forget to start your test method with "test_"!!!

Note: this unit-test is ONLY considered complete when coverage for "classes/models" = 100%
"""

#from django.test import TestCase
from books.models import Collection, Publisher, Book, Author
import unittest

def set_up_data():
        # model1: Collection
        c=Collection(name="Life Studies", code="LS")
        # model2: Publisher
        p=Publisher(name="Living Stream Ministry", code="LSM")
        # model3: Author
        a=Author(first_name="Witness", last_name="Lee", code="WL")
        # make sure all fields allowing blanks are tested
        # model4: Book without author and chapters ascribed
        b1=Book(isbn=1234567890, name="Life Study of Genesis volume 1", code="LSG1", collection=c, publisher=p)
        # model5: Book without collection ascribed
        b2=Book(isbn=1234567891, name="Life Study of Genesis volume 2", code="LSG2", chapters=25, publisher=p)
        return dict([('c', c),('p',p),('a', a),('b1',b1),('b2',b2)])

class BooksTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_models(self):
        data_dicts = set_up_data()
        self.assertTrue(Collection(data_dicts['c']))
        self.assertTrue(Publisher(data_dicts['p']))
        self.assertTrue(Author(data_dicts['a']))
        self.assertTrue(Book(data_dicts['b1']))
        self.assertTrue(Book(data_dicts['b2']))

    def test_for_foreignkey_in_Book_objects(self):
        data_dicts = set_up_data()
        self.assertEqual(data_dicts['c'].name, "Life Studies")
        self.assertEqual(data_dicts['p'].name, "Living Stream Ministry")
        self.assertEqual(data_dicts['b1'].collection.name, "Life Studies")
        self.assertIsNone(data_dicts['b1'].chapters)
        self.assertIsNone(data_dicts['b2'].collection)

    def test_unicode_functions(self):
        data_dicts = set_up_data()
        self.assertEqual('Life Studies', str(data_dicts['c']))
        self.assertEqual('Living Stream Ministry', str(data_dicts['p']))
        self.assertEqual('Witness Lee', str(data_dicts['a']))
        self.assertEqual('Life Study of Genesis volume 1', str(data_dicts['b1']))
        self.assertEqual('Life Study of Genesis volume 2', str(data_dicts['b2']))

    def tearDown(self):
        pass


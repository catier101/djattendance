"""
Refer also to books/tests and classes/tests for unit-test example
This class is intended to also serve as example on how to mock models to maintain decoupling and
also to show testing for method definitions in the model
Note: this unit-test is ONLY considered complete when coverage for "dailybread/models" = 100%
"""

from dailybread.models import Portion
from accounts.models import User
import unittest
import mock

def set_up_data():
        # foreign model: User
        u1=User(email="lifeunion@hotmail.com")
        u2=User(email="dennis@hotmail.com", firstname="Dennis", lastname="A")

        p0=Portion.today()
        # model1: Portion
        # notice each instance is made to cover different combinations of attribute values
        p1=Portion(title='Enjoyment from Class This Week')
        p1.id = id(p1)
        p2=Portion(title='The Spirit in the Bible',submitted_by= u1, approved = False)
        p3=Portion(title='Verse of the Day', text= "He who is joined to the Lord in one spirit.", ref= "1 Cor.6:17", approved= True)
        p4=Portion(submitted_by= u2, approved = False)
        # notice how this method is called here because it uses random
        p5=Portion.today()

        return dict([('p1', p1),('p2',p2),('p3', p3),('p4',p4), ('p5',p5),('p0',p0)])

class DailyBreadTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_models(self):
        data_dicts = set_up_data()
        self.assertTrue(Portion(data_dicts['p1']))
        self.assertTrue(Portion(data_dicts['p2']))
        self.assertTrue(Portion(data_dicts['p3']))
        self.assertTrue(Portion(data_dicts['p4']))
        self.assertTrue(Portion(data_dicts['p5']))

    # don't forget to test the fields that are not explicitly declared in the data set_up
    # test the fields that are not declared but left blank if they are still so
    # this test is left here for comparison with mock test below it for comparison sake
    # purpose of this test: validating the foreign key import is successful
    # either test can be used, each for its own purpose
    def test_for_foreignkey_in_DailyBread_objects(self):
        data_dicts = set_up_data()
        self.assertEqual(data_dicts['p2'].submitted_by.email, "lifeunion@hotmail.com")
        self.assertEqual(data_dicts['p2'].submitted_by.firstname, u"")
        self.assertEqual(str(data_dicts['p2'].submitted_by),"lifeunion@hotmail.com") 
        self.assertEqual(data_dicts['p4'].submitted_by.email, "dennis@hotmail.com")
        self.assertEqual(data_dicts['p4'].submitted_by.firstname, "Dennis")
        self.assertEqual(data_dicts['p4'].submitted_by.lastname, "A")

    # when using mock for term model, so any changes to Term module will not interfere this test
    # this is more ideal because unit test for class should not test "Term"
    # purpose of this test: validating the foreign key model integrity relevant to this class usage
    # notice the mock does not need set_up_data return value, thus making it cleaner
    def test_term_str(self): 
        mock_instance = mock.Mock(spec=User) 
        mock_instance.email = "jonathana@gmail.com" 
        mock_instance.firstname = "Jonathan"
        mock_instance.lastname = "A"
        self.assertEqual(User.get_full_name(mock_instance), "Jonathan A")
        self.assertEqual(User.get_short_name(mock_instance), "Jonathan")
        self.assertEqual(User.__unicode__(mock_instance), "jonathana@gmail.com")

    def test_unicode_functions(self):
        data_dicts = set_up_data()
        self.assertEqual('Enjoyment from Class This Week', str(data_dicts['p1']))
        self.assertEqual('The Spirit in the Bible', str(data_dicts['p2']))
        self.assertEqual('Verse of the Day', str(data_dicts['p3']))
        self.assertEqual(u'', data_dicts['p4'].title)

    # test all method definitions
    def test_method_def_get_absolute_url(self):
        data_dicts = set_up_data()
        self.assertEqual("/dailybread/%i/" % id(data_dicts['p1']), data_dicts['p1'].get_absolute_url())

    def test_method_def_today(self):
        data_dicts = set_up_data()
        # proving that the randomized choice always has 'approved' value = True
        #self.assertTrue(id(data_dicts['p5']) == id(data_dicts['p3']) or id(data_dicts['p5']) == id(data_dicts['p4']))
        self.assertTrue("Verse of the Day", data_dicts['p5'].title)
        # proving calling today() method when there is no objects yet return empty object
        self.assertEqual("", str(data_dicts['p0']))

    def tearDown(self):
        pass



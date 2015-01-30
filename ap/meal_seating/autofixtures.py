import random

from accounts.models import User, TrainingAssistant, Trainee
from autofixture import generators, register, AutoFixture

""" meal_seating.autofixtures borrowed from accounts

Uses django-autofixture to generate random testing data.
(https://github.com/gregmuellegger/django-autofixture/)

Create test data using the loadtestdata command, for example:
$ django-admin.py loadtestdata accounts.User:50 accounts.TrainingAssistant:5 accounts.Trainee:50

(note: generate Users before generating TAs and Trainees)
"""

class FirstNameGenerator(generators.Generator):
    """ Generates a first name, either male or female """

    def __init__(self, gender=None):
        self.gender = gender
        self.male = ['Abraham', 'Adam', 'Anthony', 'Brian', 'Bill', 'Ben', 'Calvin', 'David', 'Daniel',
                     'George', 'Henry', 'Isaac', 'Ian', 'Jonathan', 'Jeremy', 'Jacob', 'John', 'Jerry',
                     'Joseph', 'James', 'Larry', 'Michael', 'Mark', 'Paul', 'Peter', 'Phillip', 'Stephen', 
                     'Tony', 'Titus', 'Trevor', 'Timothy', 'Victor', 'Vincent', 'Winston', 'Walt']
        self.female = ['Abbie', 'Anna', 'Alice', 'Beth', 'Carrie', 'Christina' 'Danielle', 'Emma', 
                       'Emily', 'Esther', 'Felicia', 'Grace', 'Gloria', 'Helen', 'Irene', 'Joanne', 
                       'Joyce', 'Jessica', 'Kathy', 'Katie', 'Kelly', 'Linda', 'Lydia', 'Mandy', 'Mary', 
                       'Olivia', 'Priscilla', 'Rebecca', 'Rachel', 'Susan', 'Sarah', 'Stacey', 'Vivian']
        self.all = self.male + self.female

    def generate(self):
        if self.gender == 'M' or self.gender == 'Male':
            return random.choice(self.male)
        elif self.gender == 'F' or self.gender == 'Female':
            return random.choice(self.female)
        else:
            return random.choice(self.all)


class LastNameGenerator(generators.Generator):
    """ Generates a last name """

    def __init__(self):
        self.surname = ['Smith', 'Walker', 'Conroy', 'Stevens', 'Jones', 'Armstrong', 'Johnson',
                        'White', 'Stone', 'Strong', 'Olson', 'Lee', 'Forrest', 'Baker', 'Portman',
                        'Davis', 'Clark', 'Brown', 'Roberts', 'Ellis', 'Jackson', 'Marshall',
                        'Wang', 'Chen', 'Chou', 'Tang', 'Huang', 'Liu', 'Shih', 'Su', 'Song', 'Yang',
                        'Chan', 'Tsai', 'Wong', 'Hsu', 'Cheng', 'Chang', 'Wu', 'Lin', 'Yu', 'Yao', 
                        'Kang', 'Park', 'Kim', 'Choi', 'Ahn', 'Mujuni']

    def generate(self):
        return random.choice(self.surname)


class UserBrotherAutoFixture(AutoFixture):

    field_values = {
        'email' : generators.EmailGenerator(static_domain='example.com'),
        'firstname' : FirstNameGenerator(),
        'lastname' : LastNameGenerator(),
        'gender': "B",
    }
register(User, UserBrotherAutoFixture)

class UserSisterAutoFixture(AutoFixture):

    field_values = {
        'email' : generators.EmailGenerator(static_domain='example.com'),
        'firstname' : FirstNameGenerator(),
        'lastname' : LastNameGenerator(),
        'gender': "S",
    }
register(User, UserSisterAutoFixture, overwrite=True)


class TraineeAutoFixture(AutoFixture):
    spouse = Trainee()

    field_values = {
        'spouse': spouse
    }

register(Trainee, TraineeAutoFixture)


class TrainingAssistantAutoFixture(AutoFixture):
    field_values = {
    }

register(TrainingAssistant, TrainingAssistantAutoFixture)

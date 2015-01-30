import sys
import os

if __name__== "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

settingsPath = "ap.settings.dev"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settingsPath)
from django.conf import settings
from django_nose import NoseTestSuiteRunner
from optparse import OptionParser

def run_tests(*test_args, **kwargs):
    settings.NOSE_ARGS = ['--cover-package=absent_trainee_roster,accounts,attendance,books,classes,dailybread,hospitality,houses,leaveslips,lifestudies,localities,meal_seating,rooms,schedules,services,shortterm,syllabus,teams,terms,verse_parse','--cover-html']
    if not test_args:
        test_args = ['absent_trainee_roster','accounts','attendance','books','classes','dailybread','hospitality','houses','leaveslips','lifestudies','localities','meal_seating','rooms','schedules','services','shortterm','syllabus','teams','terms','verse_parse']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)
    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    run_tests(*sys.argv[1:])

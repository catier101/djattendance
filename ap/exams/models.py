import datetime

from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.timezone import timedelta

from accounts.models import Trainee
from classes.models import Class

""" exams models.py

This module allows for administering and taking of exams, including exam 
creation, editing, taking, grading, and retaking functionalities.  This module
does not handle determining class grades or generation of retake lists.

DATA MODELS:
    - Exam: Describes an exam or assessment that a trainee can take on the 
        server.  This is not used for assessments only available offline.
    - Section: describes a section of an exam.  Includes instructions and 
        the questions for the section.
    - Session: a specific instance of an exam, holds general information 
        pertaining to this take of the exam (e.g. trainee taking the exam 
        and completion statuses).
    - Responses: Holds a trainee's response to a particular section on the exam
        as well as information related to the grade or grading of the section.
    - Retake: List of Trainee/Exam pairs that indicates which combinations
        are valid for retake.
"""

class Exam(models.Model):
    training_class = models.ForeignKey(Class)
    name = models.CharField(max_length=30, blank=True)
    is_open = models.BooleanField(default=False)

    # Perhaps only to be used for retake? Should check with office.
    duration = models.DurationField(default=timedelta(minutes=90))

    # does this exam contribute to the midterm grade or to the final grade?
    CATEGORY_CHOICES = (('M', 'Midterm'),
                        ('F', 'Final'))
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    # total score is not user set--this is set as questions are added and point
    # values assigned for each question.
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __unicode__(self):
        return "%s for %s, [%s]" % (self.get_category_display(),
            self.training_class, self.training_class.term)

    # an exam is available to a particular trainee if the trainee is registered
    # for the class related to the exam and either the exam is (open and not 
    # completed by the trainee) or (trainee is on the retake list for this exam)
    def is_available(self, trainee):
        # TODO: is the trainee registered for this class?

        if Retake.objects.filter(exam=self,
                                 trainee=trainee, 
                                 is_complete=False).exists():
            return True
        
        if not self.is_open:
            return False

        if Session.objects.filter(exam=self, 
                                  trainee=trainee, 
                                  is_complete=False).exists():
            return True

        return False

    def has_trainee_completed(self, trainee):
        if Session.objects.filter(exam=self, trainee=trainee, is_complete=True).exists():
            return True
        return False

    def statistics(self):
        exams = Session.objects.filter(exam=self)
        total = 0.0
        count = 0.0

        minimum = self.total_score
        maximum = 0.0
        for exam in exams:
            if exam.is_graded:
                total = total + exam.grade
                count = count + 1
                if exam.grade < minimum:
                    minimum = exam.grade
                if exam.grade > maximum:
                    maximum = exam.grade
        stats = { 'maximum': 'n/a', 'minimum': 'n/a', 'average': 0 }
        if exams.count() > 0:
            stats['average'] = total/exams.count()
            stats['minimum'] = minimum
            stats['maximum'] = maximum
        return stats

    def _section_count(self):
        return self.sections.count()
    section_count = property(_section_count)

class Section(models.Model):
    exam = models.ForeignKey(Exam, related_name='sections')

    # Instructions
    instructions = models.TextField(null=True, blank=True)
    
    # First section in exam has a section_index of 0
    section_index = models.IntegerField(default=0)

    first_question_index = models.IntegerField(default=1)
    question_count = models.IntegerField()

    questions = HStoreField(null=True)

    def __unicode__(self):
        return "Section %s for Exam %s" % (self.section_index, self.exam.name)

class Session(models.Model):
    trainee = models.ForeignKey(Trainee)
    exam = models.ForeignKey(Exam)

    # is_complete only has meaning if the exam was submitted online
    is_submitted_online = models.BooleanField(default=True)
    is_complete = models.BooleanField(default=False)
    is_graded = models.BooleanField(default=False)

    # 0 indicates first take.
    retake_number = models.IntegerField(default=0)

    # Calculated and set when grader saves/finalizes exam grading or, if not
    # taken online, set by the grading sister manually.
    grade = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class Responses(models.Model):
    session = models.ForeignKey(Session)
    section = models.ForeignKey(Section)

    responses = HStoreField(null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class Retake(models.Model):
    trainee = models.ForeignKey(Trainee)
    exam = models.ForeignKey(Exam)
    is_complete = models.BooleanField(default=False)

    # TODO: Do we need this?
    time_opened = models.DateTimeField(auto_now_add=True)

    # TODO: to think about--
    # What about opening retake when there is an incomplete?

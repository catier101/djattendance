from django.conf import settings
from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.mail import send_mail
from django.utils.http import urlquote

from aputils.models import Vehicle, Address, EmergencyInfo
from terms.models import Term
from teams.models import Team
from houses.models import House, Bunk
from services.models import Service
from badges.models import Badge
from localities.models import Locality

""" accounts models.py
The user accounts module takes care of user accounts and
utilizes/extends Django's auth system to handle user authentication.

USER ACCOUNTS
    Because we want to use the user's email address as the unique
    identifier, we have chosen to implement a custom User model,

    Types:
        Trainee: Regular, Short-term, Commuter
        TA

    User accounts are all merged into one model for the sake of db performance
    Since the User table sits at the center of AP, constantly prefetching/pre-joining
    tables every time user is accessed is cost-prohibitive and difficult to maintain

    Other notes:
        - every Trainee is also a service worker, so those user accounts also
        have a ServiceWorker profile that contains information needed for the
        ServiceScheduler algorithm
        - before coming to the FTTA, a trainee may have come to short-term.
        These trainees will have a Short-Term profile at that time, and later
        also have a Trainee  profile when they come for the full-time.

    The merging of all tables also allow user to have multiple roles at different times in 
    their life cycle, and also allows a clean transition between roles 
    (e.g. a Short-termer who becomes a Trainee and then later a TA can keep the same 
    account throughout).
"""


class APUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """ Creates a user, given an email and a password (optional) """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=APUserManager.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Creates a super user, given an email and password (required) """

        user = self.create_user(email, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

class UserMeta(models.Model):
    maidenname = models.CharField(verbose_name=u'maiden name', max_length=30,
                                  blank=True, null=True)

    bunk = models.ForeignKey(Bunk, null=True, blank=True)

    # personal information
    married = models.BooleanField(default=False)
    spouse = models.CharField(blank=True, null=True, max_length=90)

    # refers to the user's home address, not their training residence
    address = models.ForeignKey(Address, null=True, blank=True,
                                verbose_name='home address')

    # ---------------Trainee Assistant specific--------------
    services = models.ManyToManyField(Service, related_name='services', blank=True)
    houses = models.ManyToManyField(House, related_name='houses', blank=True)

    user = models.OneToOneField('User', related_name='meta', null=True, blank=True)

class User(AbstractBaseUser, PermissionsMixin):
    """ A basic user account, containing all common user information.
    This is a custom-defined User, but inherits from Django's classes
    to integrate with Django's other provided User tools/functionality
    AbstractBaseUser provides Django's basic authentication backend.
    PermissionsMixin provides compatibility with Django's built-in permissions system.
    """

    USER_TYPES = (
        ('T', 'Training Assistant'),
        ('R', 'Regular (full-time)'),  # a regular full-time trainee
        ('S', 'Short-term (long-term)'),  # a 'short-term' long-term trainee
        ('C', 'Commuter')
    )

    type = models.CharField(max_length=1, choices=USER_TYPES)
    
    email = models.EmailField(verbose_name=u'email address', max_length=255,
                              unique=True, db_index=True)

    # to accomodate phone number such as: +(yyy)yyyyyyyyyy x.yyyyyy
    phone = models.CharField(max_length=25, null=True, blank=True)

    @property
    def username(self):
        return self.email.split('@')[0]

    badge = models.ForeignKey(Badge, blank=True, null=True)

    # All user data
    firstname = models.CharField(verbose_name=u'first name', max_length=30)
    lastname = models.CharField(verbose_name=u'last name', max_length=30)
    middlename = models.CharField(verbose_name=u'middle name', max_length=30,
                                  blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    
    GENDER = (
        ('B', 'Brother'),
        ('S', 'Sister')
    )

    gender = models.CharField(max_length=1, choices=GENDER)
    date_of_birth = models.DateField(null=True)

    @property    
    def age(self):
        # calculates age perfectly even for leap years
        return relativedelta(date.today(), self.date_of_birth).years

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Custom query manager
    objects = APUserManager()

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    @property
    def full_name(self):
        fullname = '%s %s' % (self.firstname, self.lastname)
        return fullname.strip()

    def get_short_name(self):
        return self.firstname

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return "%s, %s <%s>" % (self.lastname, self.firstname, self.email)

    # ---------------Trainee specific--------------
    # Terms_attended can exist for every user but curent_term does not necessarily make sense for a TA for example
    terms_attended = models.ManyToManyField(Term)   
    current_term = models.IntegerField(default=1, null=True, blank=True)
    
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    TA = models.ForeignKey('self', related_name='training_assistant', null=True, blank=True)
    mentor = models.ForeignKey('self', related_name='mentee', null=True,
                               blank=True)

    locality = models.ManyToManyField(Locality, blank=True)

    team = models.ForeignKey(Team, null=True, blank=True)
    house = models.ForeignKey(House, null=True, blank=True)

    # flag for trainees taking their own attendance
    # this will be false for 1st years and true for 2nd with some exceptions.
    self_attendance = models.BooleanField(default=False)

    # TODO: will return True if the trainee has the designated service to enter exam scores/grade
    def is_designated_grader(self):
        return True

    def get_outstanding_discipline(self):
        o_discipline = []
        for discipline in self.discipline_set.all():
            if not discipline.is_completed():
                o_discipline.append(discipline)
        return o_discipline

    # Optional meta field to lighten each user object
    # meta = models.OneToOneField(UserMeta, related_name='user', null=True, blank=True)


class TraineeManager(models.Manager):
    def get_queryset(self):
        return super(TraineeManager, self).get_queryset().filter(models.Q(type='R') | models.Q(type='S') | models.Q(type='C'))

class Trainee(User):

    def __unicode__(self):
        return "%s, %s <%s>" % (self.lastname, self.firstname, self.email)

    class Meta:
        proxy = True

    objects = TraineeManager()

class TAManager(models.Manager):
    def get_queryset(self):
        return super(TAManager, self).get_queryset().filter(type='T')

class TrainingAssistant(User):
    class Meta:
        proxy = True
    
    objects = TAManager()

# Statistics / records on trainee (e.g. attendance, absences, service/fatigue level, preferences, etc)
class Statistics(models.Model):
    trainee = models.OneToOneField(User, related_name='statistics', null=True, blank=True)

    # String containing book name + last chapter of lifestudy written ([book_id]:[chapter], Genesis:3)
    latest_ls_chpt = models.CharField(max_length=400, null=True, blank=True)

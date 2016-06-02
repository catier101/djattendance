from ap.settings import local
from django.core.management import setup_environ
setup_environ(local)

from ss.models import *
from services.models import *
from datetime import datetime

sc = Scheduler()
sc.test()
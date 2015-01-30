from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ('django_extensions',
                   'autofixture',
                   'debug_toolbar',
                   'django_reset',
                   'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djattendance',
        'USER': 'ap',
        'PASSWORD': '4livingcreatures',
        'HOST': 'localhost',
        'PORT': '',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',  # use local jquery (for offline development)
}


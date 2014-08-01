from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += ('django_extensions',
                   'debug_toolbar',
                   'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djattendance',
        'USER': 'ap',
        'PASSWORD': '',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

INTERNAL_IPS = ('127.0.0.1',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',  # use local jquery (for offline development)
}

MAX_UPLOAD_SIZE = 20971520  # 20MB
CONTENT_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']  # .pdf, .jpeg and .png

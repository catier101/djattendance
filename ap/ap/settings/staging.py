from .base import *

DEBUG = True

import dj_database_url

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/ap/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'ap/static'),
)



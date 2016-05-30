from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
'''
  For the following to work, you need to:
  export DATABASE_URL='postgres://{{username}}:{{password}}@localhost:5432/{{database}}'
'''
DATABASES = {'default' : dj_database_url.config()}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
SITE_ROOT = os.path.dirname(os.path.abspath(__name__))
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

CELERYD_LOG_LEVEL = 'WARNING'
CELERYBEAT_LOG_LEVEL = 'WARNING'

# Communicating with firewall for granting web access requests
HOST = "10.0.8.20" # hostname or ip address of the firewall (add to /etc/hosts)
PORT = 12345 # server port of application which listens for commands on the firewall

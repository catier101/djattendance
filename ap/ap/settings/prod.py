from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

ADMINS = (
    ('Attendance Project', 'attendanceproj@gmail.com'),
)
MANAGERS = ADMINS

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'AP <ap@ftta.com>'
SERVER_EMAIL = 'AP Server <server@ftta.com>'

# Set unlimited persistent connections
CONN_MAX_AGE = 'None'

# Parse database configuration from $DATABASE_URL
import dj_database_url
'''
  For the following to work, you need to:
  export DATABASE_URL='postgres://{{username}}:{{password}}@localhost:5432/{{database}}'
'''
DATABASES = {'default' : dj_database_url.config()}

SECRET_KEY = os.environ['SECRET_KEY']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

CELERYD_LOG_LEVEL = 'WARNING'
CELERYBEAT_LOG_LEVEL = 'WARNING'

# Communicating with firewall for granting web access requests
HOST = "10.0.8.20" # hostname or ip address of the firewall (add to /etc/hosts)
PORT = 12345 # server port of application which listens for commands on the firewall

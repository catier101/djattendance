from django.conf import settings
import os

SITE_ROOT = os.path.dirname(os.path.abspath(__name__))

if __name__ == '__main__':
  apps = ' '.join([ app for app in settings.INSTALLED_APPS if not "django" in app ])
  print 'Running make migrations on: ', apps
  print '--------------------'

  os.system(os.path.join(SITE_ROOT, 'ap', 'manage.py') + ' makemigrations ' + apps)

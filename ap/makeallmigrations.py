from django.conf import settings
import os

if __name__ == '__main__':
  apps = ' '.join([ app for app in settings.INSTALLED_APPS if not "django" in app ])
  print 'Running make migrations on: ', apps
  print '--------------------'

  os.system(os.path.join(settings.SITE_ROOT, 'manage.py') + ' makemigrations ' + apps)

import random
import sys

from django.conf.global_settings import MIDDLEWARE_CLASSES

try:
    from lit.settings.base import *
except ImportError:
    sys.exit(-1)

DEBUG = True

SECRET_KEY = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") \
                      for i in range(50)])

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.extend(['django_nose', 'debug_panel'])

MIDDLEWARE_CLASSES.extend(
    ['debug_toolbar.middleware.DebugToolbarMiddleware', 'debug_panel.middleware.DebugPanelMiddleware', ])

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=users',  # ,repositories,branches,commits,permissions
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

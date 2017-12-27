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

INSTALLED_APPS.extend(['django_nose', 'debug_toolbar'])

MIDDLEWARE_CLASSES.extend(
    ['debug_toolbar.middleware.DebugToolbarMiddleware', ])

MIDDLEWARE.extend(
    ['debug_toolbar.middleware.DebugToolbarMiddleware', ])

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=users,repositories',  # ,branches,commits,permissions
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('localhost', '127.0.0.1',)
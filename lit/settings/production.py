import sys

try:
    from lit.settings.base import *
except ImportError:
    sys.exit(-1)

DEBUG = False

SECRET_KEY = os.environ['LIT_NOTHING_TO_SEE_HERE']

ALLOWED_HOSTS = ['litvcs.win', 'www.litvcs.win']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['LIT_DB_NAME'],
        'USER': os.environ['LIT_DB_USERNAME'],
        'PASSWORD': os.environ['LIT_DB_PASSWORD'],
        'HOST': os.environ['LIT_DB_HOST'],
        'PORT': os.environ['LIT_DB_PORT'],
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

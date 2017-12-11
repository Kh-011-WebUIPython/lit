"""
WSGI config for lit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if 'LIT_NOTHING_TO_SEE_HERE' in os.environ:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lit.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lit.settings.development")

application = get_wsgi_application()

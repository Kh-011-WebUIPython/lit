#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if 'LIT_NOTHING_TO_SEE_HERE' in os.environ:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lit.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lit.settings.development")

    if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
        os.mkdir('logs')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)

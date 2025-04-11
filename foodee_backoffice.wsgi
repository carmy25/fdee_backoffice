import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' command.
APP_NAME = os.environ.get("FLY_APP_NAME")
if APP_NAME:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
		      'foodee_backoffice.settings.fly')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
		      'foodee_backoffice.settings.dev')

# Get the WSGI application for use with Gunicorn.
application = get_wsgi_application()

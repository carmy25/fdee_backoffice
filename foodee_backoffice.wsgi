import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' command.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodiee_backoffice.settings')

# Get the WSGI application for use with Gunicorn.
application = get_wsgi_application()

import sentry_sdk
import os
import dj_database_url
from .base import *

APP_NAME = os.environ.get("FLY_APP_NAME")
APP_VERSION = os.environ.get("FLY_APP_VERSION")
APP_REVISION = os.environ.get("FLY_APP_REVISION")
APP_REGION = os.environ.get("FLY_REGION")
APP_INSTANCE = os.environ.get("FLY_INSTANCE")
APP_INSTANCE_MEMORY = os.environ.get("FLY_INSTANCE_MEMORY")
APP_INSTANCE_CPU = os.environ.get("FLY_INSTANCE_CPU")
APP_INSTANCE_COUNT = os.environ.get("FLY_INSTANCE_COUNT")
APP_INSTANCE_STORAGE = os.environ.get("FLY_INSTANCE_STORAGE")
APP_INSTANCE_REGION = os.environ.get("FLY_REGION")

# running on fly.io
print(f"Running on fly.io: {APP_NAME}")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
# print env variables for debugging
ALLOWED_HOSTS = [f"{APP_NAME}.fly.dev"]
CSRF_TRUSTED_ORIGINS = [f"https://{APP_NAME}.fly.dev"]

DATABASES["default"] = dj_database_url.config(
    conn_max_age=600)
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
    'rest_framework.authentication.TokenAuthentication'
]
REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    'rest_framework.permissions.IsAuthenticated'
]
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    'rest_framework.renderers.JSONRenderer'
]
REST_FRAMEWORK["DEFAULT_PARSER_CLASSES"] = [
    'rest_framework.parsers.JSONParser'
]
REST_FRAMEWORK["UNICODE_JSON"] = True
REST_FRAMEWORK["DEFAULT_PAGINATION_CLASS"] = 'rest_framework.pagination.PageNumberPagination'
REST_FRAMEWORK["PAGE_SIZE"] = 10
REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"] = [
    'django_filters.rest_framework.DjangoFilterBackend']

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },

    "default": {
        "BACKEND": 'foodee_backoffice.storage.TigrisMediaStorage',
        "OPTIONS": {
            'querystring_auth': False,
            'bucket_name': os.environ.get("BUCKET_NAME") or '',
        },
    },
}

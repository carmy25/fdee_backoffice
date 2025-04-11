"""
Django settings for foodee_backoffice project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import sentry_sdk

import dj_database_url

from storages.backends.s3boto3 import S3Boto3Storage


class TigrisMediaStorage(S3Boto3Storage):

    def url(self, name):
        return f"https://{self.bucket_name}.fly.storage.tigris.dev/{name}"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURE_DIRS = [BASE_DIR / "fixtures"]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6$@12h^4)zqn#y3s7u*ok)5qm0o2veui4k7bn_tr-1f78pe^)_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
APPEND_SLASH = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework.authtoken',

    'adminplus',


    "user.apps.UserConfig",
    "order.apps.OrderConfig",
    "place.apps.PlaceConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "foodee_backoffice.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodee_backoffice.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {
            "NAME": ":memory:",
        }
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "uk-ua"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'EXCEPTION_HANDLER': 'order.exceptions.custom_exception_handler',
    'UNICODE_JSON': True,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ]
}


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

if APP_NAME is not None:
    # running on fly.io
    print(f"Running on fly.io: {APP_NAME}")
    import sentry_sdk

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
            "BACKEND": 'settings.TigrisMediaStorage',
            "OPTIONS": {
                'querystring_auth': False,
                'bucket_name': os.environ.get("BUCKET_NAME"),
            },
        },
    }

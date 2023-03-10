import base64
import json
import os

import dj_database_url
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", "p)za_c9ew*tjhr6-2!9x$^4*yxdjk4chzx=8%h#55eepeca5az")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", "true")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", ["*"])

STATIC_URL = "/publisher/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATE_DIRS = (os.path.join(BASE_DIR, "app/templates"),)

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",

    "rest_framework",

    "apps.articles",
    "apps.xrpl",
)

MIDDLEWARE = (
    # 'apps.core.middleware.DisableCSRF',
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "apps.xrpl.middleware.account.AccountMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",

)

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "libraries": {},
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

# WSGI_APPLICATION = 'app.wsgi.application'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_HOST", "redis://redis-master.redis:6379/0"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "auth",
    },
    "translations_cache": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_CONNECTION",
            "postgres://postgres:postgres@localhost:5432/de-media",
        ),
        conn_max_age=env.int("DATABASE_CONN_MAX_AGE", 120),
    )
}

USE_I18N = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

DATE_FORMAT = "d-m-Y"
USE_L10N = False

SITE_ID = 1

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "apps.core.api.pagination.BasePagination",
    "PAGE_SIZE": 100,
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    # "DEFAULT_FILTER_BACKENDS": (
    #     "apps.core.filters_backend.RestFrameworkFilterBackend",
    # ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# Logging

SYSTEM_LOGGER_NAME = "system"
LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {"format": "%(name)-15s %(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        SYSTEM_LOGGER_NAME: {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security": {"propagate": True, },
    },
}

SERVICE_PREFIX = env("SERVICE_PREFIX", "publisher")

USE_TZ = True
TIME_ZONE = "Europe/Luxembourg"

SWAGGER_SETTINGS = {
    "VALIDATOR_URL": None,
}


MCS_API_KEY = env.str("MCS_API_KEY")
MCS_ACCESS_TOKEN = env.str("MCS_ACCESS_TOKEN")
ONCHIN_PRIVATE_KEY = env.str("ONCHIN_PRIVATE_KEY")
ONCHIN_RPC_ENDPOINT = env.str("ONCHIN_RPC_ENDPOINT", None) or "https://polygon-bor.publicnode.com"


WALLET_CREDS = json.loads(base64.b64decode(env.str("WALLET_CREDS", "")))

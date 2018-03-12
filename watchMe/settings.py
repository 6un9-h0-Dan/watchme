"""
Django settings for watchMe project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import socket
import yara
from ConfigParser import RawConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!

if socket.gethostname().startswith('ruinedsec'):
    DEBUG = True
else:
    DEBUG = False


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'APIs',
    'django_celery_results',
    'djcelery_email',
    'django_celery_beat',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'watchMe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'watchMe.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Qatar'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'


CELERY_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_PID_LOGS = os.path.join(BASE_DIR, 'celery_pids_logs')

if not os.path.exists(CELERY_PID_LOGS):
    os.makedirs(CELERY_PID_LOGS)

yara_rules = yara.compile(filepath=os.path.join(BASE_DIR, 'shawky.yara'))

if DEBUG:
    ALLOWED_HOSTS = ["*"]

    SECRET_KEY = ')=y)t@hwf%f!*ww4!ae6&3gn$2%ow#-%3vmvo42l$@+-qoo$2e'

    EMAIL_HOST = 'localhost'
    EMAIL_HOST_USER = None
    EMAIL_HOST_PASSWORD = None
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

    SERVER_EMAIL = 'info@localhost'
    ALERT_EMAIL_FROM = "WatchME <watchMe@localhost>"
    ALERT_EMAIL_TO = ["admin@localhost"]
    ADMINS = (
        ('Admin', 'admin@localhost'),
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    CELERY_BROKER_URL = 'amqp://watcher:Raya_123!@localhost:5672/watcher'
else:
    # Security headers
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # SECURE_CONTENT_TYPE_NOSNIFF = True    # to be added on the proxy
    # SECURE_BROWSER_XSS_FILTER = True      # o be added on the proxy
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
    # CSRF_COOKIE_HTTPONLY = True
    # X_FRAME_OPTIONS = "DENY"

    # FIXME: MySQL does not allow unique CharFields to have a max_length > 255
    SILENCED_SYSTEM_CHECKS = ['mysql.E001']

    config = RawConfigParser()
    config.read('%s/production_settings.ini' % os.path.expanduser('~'))

    ALLOWED_HOSTS = map(
        str.strip, config.get('general', 'ALLOWED_HOSTS').split(','))

    ALERT_EMAIL_FROM = config.get('email', 'ALERT_EMAIL_FROM')
    ALERT_EMAIL_TO = map(
        str.strip, config.get('email', 'ALERT_EMAIL_TO').split(','))
    SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')

    ADMINS = (
        ('Ahmed Shawky', config.get('email', 'ADMIN_EMAIL')),
    )

    SECRET_KEY = config.get('secrets', 'SECRET_KEY')

    EMAIL_HOST = config.get('email', 'EMAIL_HOST')

    CELERY_BROKER_URL = config.get('celery', 'CELERY_BROKER_URL')

    DATABASE_NAME = config.get('database', 'DATABASE_NAME')
    DATABASE_USER = config.get('database', 'DATABASE_USER')
    DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
    DATABASE_HOST = config.get('database', 'DATABASE_HOST')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': DATABASE_HOST,
        }
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
            },
        },
        'handlers': {
            # Send all messages to console
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
            },
            # Warning messages are sent to admin emails
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },
        },
        'loggers': {
            # This is the "catch all" logger
            '': {
                'handlers': ['console', 'mail_admins', ],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

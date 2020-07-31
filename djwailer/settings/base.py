# -*- coding: utf-8 -*-

"""Django settings for project."""


import os


DEBUG = True
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS

SECRET_KEY = None
ALLOWED_HOSTS = []
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True
TIME_ZONE = 'America/Chicago'
DEFAULT_CHARSET = 'cp1252'
FILE_CHARSET = 'cp1252'
SERVER_URL = ''
API_URL = '{0}/{1}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{0}'.format(SERVER_URL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP = os.path.basename(BASE_DIR)
ROOT_URL = ''
BRIDGE_URL = ''
ROOT_URLCONF = 'djwailer.urls'
WSGI_APPLICATION = 'djwailer.wsgi.application'
MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = ''
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DATABASES = {
    'default': {
        'HOST': '',
        'PORT': '',
        'NAME': '',
        'ENGINE': '',
        'USER': '',
        'PASSWORD': None,
    },
    'livewhale': {
        'HOST': '',
        'PORT': '',
        'NAME': '',
        'ENGINE': '',
        'USER': '',
        'PASSWORD': None,
        'OPTIONS': {
            'charset': 'latin1',
            'use_unicode': False,
            'ssl': {'ca': ''},
        },
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'djwailer.core',
    'djwailer.bridge',
    # needed for template tags
    'djtools',
    # honeypot for admin attacks
    'admin_honeypot',
    # sign in as a user
    'loginas',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
            '/data2/django_templates/djkatara/',
            '/data2/django_templates/djcher/',
            '/data2/django_templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = None
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# SMTP & Email settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = None
EMAIL_USE_TLS = True
EMAIL_PORT = 0
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{0}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = ''
SESSION_COOKIE_AGE = 86400
# App settings
BRIDGE_CATEGORY = 30
BRIDGE_USER = 7
BRIDGE_GROUP = 94
BRIDGE_TOP_STORY_TAG = '912'
BRIDGE_NEW_TAG = '988'
BRIDGE_STUDENT = ''
BRIDGE_COMMS = ''
PROFILES_TO_LIST = []
# logging
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), 'logs/')
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'djwailer': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'core': {
            'handlers': ['logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local import *", we use exec so that
# local has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

phile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local.py')
if os.path.exists(phile):
    import imp
    import sys
    module_name = '{0}.settings.local'.format(PROJECT_APP)
    module = imp.new_module(module_name)
    module.__file__ = phile
    sys.modules[module_name] = module
    exec(open(phile, 'rb').read())

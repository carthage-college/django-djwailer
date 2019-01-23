"""
Django settings for djwailer project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Debug
#DEBUG = False
DEBUG = True
ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS

SECRET_KEY = ''
ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True # LiveWhale stores dates as UTC

# 13 Feb 2014
#DEFAULT_CHARSET = 'latin1'
#FILE_CHARSET = 'latin1'

# works! 26 March 2015
DEFAULT_CHARSET = 'cp1252'
FILE_CHARSET = 'cp1252'

# commented out prior to 13 Feb 2014
#DEFAULT_CHARSET = 'utf-8'
#FILE_CHARSET = 'utf-8'

SERVER_URL = ""
API_URL = "%s/%s" % (SERVER_URL, "api")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(__file__)
ROOT_URL = "/djwailer/"
ROOT_URLCONF = 'djwailer.urls'
WSGI_APPLICATION = 'djwailer.wsgi.application'
MEDIA_ROOT = ''
STATIC_ROOT = ''
STATIC_URL = "/static/"
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'djforms',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {'charset':'latin1','use_unicode':False,}
    },
    'livewhale': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'livewhale_staging',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': ''
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
    'djwailer',
    'djwailer.core',
    'djwailer.bridge',
    'djtools',
)

MIDDLEWARE_CLASSES = (
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
            "/data2/django_projects/djwailer/templates/",
            "/data2/django_templates/djkatara/",
            "/data2/django_templates/djcher/",
            "/data2/django_templates/django-djskins/",
            "/data2/livewhale/includes/",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':DEBUG,
            'context_processors': [
                "djtools.context_processors.sitevars",
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            #'loaders': [
            #    # insert your TEMPLATE_LOADERS here
            #]
        },
    },
]

# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/django_directory_cache',
        #'TIMEOUT': 60*20,
        #'KEY_PREFIX': "DIRECTORY_",
        #'OPTIONS': {
        #    'MAX_ENTRIES': 80000,
        #}
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = '636'
LDAP_PROTOCOL = "ldaps"
LDAP_BASE = ""
LDAP_USER = ""
LDAP_PASS = ""
LDAP_EMAIL_DOMAIN = ""
LDAP_OBJECT_CLASS = ""
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR=""
# SMTP & Email settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=""
CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS = {}
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/djwailer/accounts/login/'
LOGOUT_URL = '/djwailer/accounts/logout/'
LOGIN_REDIRECT_URL = '/djwailer/'
USE_X_FORWARDED_HOST = True
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN=".carthage.edu"
SESSION_COOKIE_NAME ='django_carthage_cookie'
SESSION_COOKIE_AGE = 86400
# App settings
BRIDGE_CATEGORY=0
BRIDGE_USER=0
BRIDGE_GROUP = 0
BRIDGE_TOP_STORY_TAG=''
BRIDGE_NEW_TAG=''
BRIDGE_STUDENT = []
BRIDGE_COMMS = []
# logging
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'djwailer': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'core': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
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
    }
}

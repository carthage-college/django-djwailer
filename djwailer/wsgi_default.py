"""
WSGI config for djwailer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/usr/local/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djwailer.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/var/cache/python/.python-eggs")
os.environ.setdefault("TZ", "America/Chicago")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


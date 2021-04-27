# -*- coding: utf-8 -*-
import os, sys
import datetime

# env
sys.path.append('/usr/local/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djwailer.settings")

from django.conf import settings
from djwailer.core.models import LivewhaleProfiles,LivewhaleUsers
from djtools.utils.mail import send_mail

"""
Shell script that sends out an email to communications
to notify them of any profile changes
"""

def main():
    # mail stuff
    BCC = settings.MANAGERS
    FROM = "Carthage Bridge <bridge@carthage.edu>"
    days = 1
    now = datetime.date.today()
    past = now - datetime.timedelta(days=days)

    profiles = LivewhaleProfiles.objects.using('livewhale').filter(last_modified__gte=past)

    for p in profiles:
        if p.last_user:
            p.modified_by = LivewhaleUsers.objects.using('livewhale').get(pk=p.last_user)

        #print p.firstname
        #print p.lastname
        #print p.username
        #print p.modified_by.username,p.modified_by.firstname,p.modified_by.lastname
        #print "https://www.carthage.edu/live/profiles/%s/" % p.id
        #print "+++++++++++++++++++++++"

    # send mail
    if len(profiles) > 0:
        subject = "[Profiles] Modified in the past 24 hours"
        request = None
        send_mail(
            request, settings.PROFILES_TO_LIST, subject, FROM,
            "livewhale/profiles/watcher_email.html", profiles, BCC
        )


if __name__ == "__main__":
    sys.exit(main())

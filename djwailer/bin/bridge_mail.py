# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_current/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djwailer.settings")

from django.conf import settings
from django.db.models import Q

from djwailer.core.models import LivewhaleEvents, LivewhaleNews, tags_list, TAGS
from djwailer.bridge.views import fetch_newsletter, NOW

from djtools.utils.mail import send_mail

from optparse import OptionParser

"""
Shell script that sends out email to students/faculty/staff
with news and events from LiveWhale data

Cron delivery for testing at:

Monday @ 7h
Wednesday @ 7h
Friday @ 7h
"""

# set up command-line options
desc = """
Accepts as input y or n, to send email to everybody or to
default, debug address.
"""

parser = OptionParser(description=desc)
parser.add_option("-s", "--send", help="Dry run or not? y/n.", dest="send")

def main():
    # mail stuff
    if send=="y":
        BCC = ["bridge@carthage.edu",]
        TO_LIST = [
            "faculty-staff@lists.carthage.edu",
            "student@lists.carthage.edu"
        ]
    else:
        BCC = settings.MANAGERS
        #TO_LIST = ["larry@carthage.edu",]
        TO_LIST = [
            "bbeyer@carthage.edu",
            "eyoung@carthage.edu",
            "tapplegarth@carthage.edu"
        ]
    FROM = "Carthage Bridge <bridge@carthage.edu>"
    settings.DEFAULT_CHARSET = 'utf-8'
    settings.FILE_CHARSET = 'utf-8'
    settings.DATABASES["livewhale"]['OPTIONS'] = {'charset': 'latin1', 'use_unicode': False}

    data = fetch_newsletter()
    # send mail
    subject = "[The Bridge] News & Events: %s" % (NOW.strftime("%A, %B %d, %Y"))
    request = None
    send_mail(
        request, TO_LIST, subject, FROM,
        "bridge/email.html", data, BCC
    )

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    send = options.send
    if not send:
        print "'y' or 'n' as to whether or not this is a dry run.\n"
        parser.print_help()
        exit(-1)

    sys.exit(main())

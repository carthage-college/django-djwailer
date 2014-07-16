from django.core import serializers
from optparse import OptionParser

from djwailer.core.models import LivewhaleCourseCatalog, LivewhaleProfilesFields

import urllib, json, sys

"""
Shell script that manages data exported from
Informix in JSON format and imported into MySQL.

URL structure:

Physics
http://www.carthage.edu/jenzabar/api/catalog/UG14/PHY/
http://www.carthage.edu/jenzabar/api/catalog/UG14/
All Graduate Courses
http://www.carthage.edu/jenzabar/api/catalog/GR14/

OJO: after importing the UG14 courses, you have to comment out
the delete portion of the script and then run the GR14 URL.
"""

#set up command-line options
desc = """
Takes a URL and grabs JSON data for processing
"""

parser = OptionParser(description=desc)
parser.add_option("-u", "--url", help="url that returns JSON data", dest="earl")

def get_profile_id(email):
    try:
        profile = LivewhaleProfilesFields.objects.filter(
            fid=37
        ).filter(value=email).order_by('pid')[0]
        pid = profile.pid
    except:
        pid = None
    return pid

def main():
    # read the json data from URL
    response =  urllib.urlopen(earl)
    data = response.read()
    jsonResponse = serializers.deserialize("json", data)
    # delete the current catalog of courses
    LivewhaleCourseCatalog.objects.using('livewhale').all().delete()
    # here we cycle through the objects and make the updates
    # we can without having to save
    for s in jsonResponse:
        if s.object.max_hrs == s.object.min_hrs:
            s.object.credits = int(s.object.max_hrs)
        else:
            s.object.credits = "%s-%s" % (
                int(s.object.min_hrs), int(s.object.max_hrs)
            )
        name = "%s %s" % (s.object.firstname, s.object.lastname)
        pid = get_profile_id(s.object.email)
        if pid:
            p = '<a href="/live/profiles/%s-%s-%s/">%s</a>' % (
                pid, s.object.firstname, s.object.lastname, name
            )
        else:
            p = name
        s.object.instructors = p
        s.save(using="livewhale")

    # search for duplicates and concatenate instructors and terms
    # from duplicates and then remove them

    for c in LivewhaleCourseCatalog.objects.using('livewhale').values_list(
            'crs_no', flat=True
        ).distinct():
        dupes =  LivewhaleCourseCatalog.objects.using('livewhale').filter(
            pk__in=LivewhaleCourseCatalog.objects.filter(crs_no=c).values_list(
                'id', flat=True
            )
        )
        course = dupes[0]
        if len(dupes) > 1:
            # we put professors and terms in lists so we can check for
            # duplicates and sort alphabetically
            profis = [course.instructors,]
            terms = [course.txt,]
            # skip the 0 index since that is the course we will update
            # while removing the other dupes
            for d in dupes[1:]:
                if d.instructors not in profis:
                    profis.append(d.instructors)
                if d.txt not in terms:
                    terms.append(d.txt)
                d.delete()
            course.instructors = ', '.join(sorted(profis))
            course.terms = ', '.join(sorted(terms))
        else:
            course.terms = course.txt
        if course.instructors == "" or course.instructors == " ":
            course.instructors = "Staff"
        course.save(using="livewhale")

######################
# shell command line
######################

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    earl = options.earl
    if not earl:
        print "You must provide a URL\n"
        parser.print_help()
        exit(-1)

    sys.exit(main())

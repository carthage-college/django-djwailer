from django.core import serializers

from djwailer.core.models import LivewhaleCourseCatalog, LivewhaleProfilesFields

import urllib, json, sys

"""
Shell script that manages data exported from
Informix in JSON format and imported into MySQL.

URL structure:

Physics
https://www.carthage.edu/jenzabar/api/catalog/UG15/PHY/
ALL Undergraduate Courses
https://www.carthage.edu/jenzabar/api/catalog/UG15/
All Graduate Courses
https://www.carthage.edu/jenzabar/api/catalog/GR15/

OJO:

execute destroy.py to dump the catalog.

then, after importing the UG* courses:

python bin/json_munger.py --url=https://www.carthage.edu/jenzabar/api/catalog/UG15/

execute the following SQL command:

update livewhale_course_catalog set disc="" where dept="EDU"

then run the GR* URL.

python bin/json_munger.py --url=https://www.carthage.edu/jenzabar/api/catalog/GR15/EDU/

then execute:

update livewhale_course_catalog set disc="MED" where dept="EDU" and disc="EDU"
update livewhale_course_catalog set disc="EDU" where dept="EDU" and disc=""
"""

#set up command-line options
desc = """
Takes a URL and grabs JSON data for processing
"""
import django
django.setup()

import argparse

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-u", "--url",
    help="The URL that returns JSON data",
    dest="earl"
)

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
    # here we cycle through the objects and execute some updates
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
        s.object.id = None
        s.save(using="livewhale")
    # search for duplicates and concatenate instructors and terms
    # from duplicates and then remove them.
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
            # oddly, txt is missing from time to time and becomes None
            # which causes the join on sorted(terms) below to barf
            terms = []
            if course.txt and course.txt != "":
                terms.append(course.txt)
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
    args = parser.parse_args()
    earl = args.earl

    if not earl:
        print "You must provide a URL\n"
        parser.print_help()
        exit(-1)
    sys.exit(main())


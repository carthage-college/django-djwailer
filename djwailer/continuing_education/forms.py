from django import forms
from django.db import connections
from django.utils.timezone import localtime
from django.utils.dateformat import DateFormat

from djwailer.core.models import LivewhaleEvents
from djtools.fields import STATE_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

HEAR_ABOUT =  [
    ('Education/Career Fair', 'Education/Career Fair'),
    ('Radio', 'Radio'),
    ('Newspaper', 'Newspaper'),
    ('Direct Mail', 'Direct Mail'),
    ('E-mail', 'E-mail'),
    ('Internet Search', 'Internet Search'),
    (
        'Information Session/Admissions Event',
        'Information Session/Admissions Event'
    ),
    ('Associate/Friend/Colleague', 'Associate/Friend/Colleague'),
    ('Referral-Advisor-Employer', 'Referral-Advisor-Employer'),
    ('I am a Carthage Graduate', 'I am a Carthage Graduate'),
    ('Carthage Website', 'Carthage Website'),
    ('Other', 'Other'),
]

# dictionary name corresponds to URL slug
STYPES = {
    "information-session":712,
    "graduate-studies":715,
    "undergraduate-studies":713,
    "master-social-work":714,
    "paralegal":582
}

class InfoSessionForm(forms.Form):
    event = forms.ChoiceField(choices=())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField(label="Street Address")
    city = forms.CharField()
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(required=False,help_text="Format: XXX-XXX-XXXX")
    hear_about = forms.CharField(
        label="How did you hear about the program?",
        widget=forms.Textarea
    )

    def __init__(self,session_type,*args,**kwargs):
        super(InfoSessionForm,self).__init__(*args,**kwargs)
        cursor = connections['livewhale'].cursor()
        sql = """
            SELECT
                id,title,date_dt
            FROM
                livewhale_events
            WHERE
                id IN (
                    select id2 from livewhale_tags2any where id1=%s
                )
            AND
                id IN (
                    select id2 from livewhale_tags2any where id1=%s
                )
            AND
                date_dt > DATE(NOW())
            ORDER BY
                date_dt
        """ % (STYPES["information-session"],STYPES[session_type])
        cursor.execute(sql)
        # Wed. May 07, 2014 at 06pm (Master of Education & ACT Info Session)
        choices = [('','---choose a date---')]
        for event in cursor.fetchall():
            lc = localtime(event[2])
            df = DateFormat(lc)
            day = df.format('D')
            date = df.format('M d, Y')
            time = df.format('h:ia')
            title = "%s. %s at %s (%s)" % (day, date, time ,event[1])
            choices.append((event[0],title))
        self.fields['event'].choices = choices

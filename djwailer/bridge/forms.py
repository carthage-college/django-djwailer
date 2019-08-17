from django import forms
from django.conf import settings

from djwailer.core.models import LivewhaleEvents, LivewhaleNews, CATEGORIES

from djtools.fields.time import KungfuTimeField

from htmllaundry import sanitize

if settings.DEBUG:
    REQ = {'class': 'required'}
else:
    REQ = {'class': 'required','required': 'required'}

SEND_TO = (
    ('','---------'),
    (False,'[TEST] Communications'),
    (True,'[LIVE] Campus Community'),
)
import logging
#logger = logging.getLogger(__name__)
logger = logging.getLogger('debug_logger')


class EventSubmissionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255
    )
    description = forms.CharField(
        widget=forms.Textarea
    )
    location = forms.CharField(
        max_length=255, required=False
    )
    start_date = forms.DateField()
    end_date = forms.DateField()
    start_time = KungfuTimeField(
        label="Event starts at",
        help_text="(Format HH:MM am/pm)", required=False
    )
    end_time = KungfuTimeField(
        label="Event Ends at",
        help_text="(Format HH:MM am/pm)", required=False
    )
    category = forms.CharField(
        widget=forms.Select(choices=CATEGORIES, attrs=REQ)
    )
    entity = forms.CharField(
        label="Sponsoring department, office, or student organization",
        max_length=255, required=True
    )
    contact_information = forms.CharField(
        required=True, widget=forms.Textarea,
        help_text="""
            Who should people contact for more information?
            Please include name and phone or email.
        """
    )

    class Meta:
        model = LivewhaleEvents
        fields = (
            'title','description','location','start_date','end_date',
            'start_time','end_time','category','entity','contact_information'
        )

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if (start_date and end_date) and start_date > end_date:
            raise forms.ValidationError("""
                You must pick an end date later than the start date.
            """)
        return end_date

    def clean_end_time(self):
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        if (start_time and end_time) and start_time > end_time:
                raise forms.ValidationError("""
                    You must pick an end time later than the start time.
                """)
        return end_time

    def clean(self):
        cd = self.cleaned_data
        description = cd.get('description')
        if description:
            if cd.get('entity'):
                entity = '<h4>SPONSORING DEPARTMENT, OFFICE, OR ORGANIZATION:</h4>'
                entity += '<p>{}</p>'.format(cd['entity'])
                description += entity
            if cd.get('contact_information'):
                contact = '<h4>FOR MORE INFORMATION, CONTACT:</h4>'
                contact += '<p>{}</p>'.format(cd['contact_information'])
                description += contact
            cd['description'] = sanitize(description)
        return cd


class NewsSubmissionForm(forms.ModelForm):
    headline = forms.CharField(max_length=255)
    body = forms.CharField(
        label="Body of Article", widget=forms.Textarea
    )
    summary = forms.CharField(
        label = """
            Short Summary (One-or two-sentence summary of your
            news that will serve as an introduction to your
            article)""",
        widget=forms.Textarea,
    )
    category = forms.CharField(
        widget=forms.Select(choices=CATEGORIES, attrs=REQ)
    )
    entity = forms.CharField(
        label="Sponsoring department, office, or student organization",
        max_length=255, required=False
    )
    contact_information = forms.CharField(
        required=False, widget=forms.Textarea,
        help_text="""
            Who should people contact for more information?
            Please include name and phone or email.
        """
    )

    class Meta:
        model = LivewhaleNews
        fields = (
            'headline','body','summary','category','entity','contact_information'
        )

    def clean(self):
        cd = self.cleaned_data
        body = cd.get('body')
        if body:
            if cd.get('entity'):
                entity = '<h4>SPONSORING DEPARTMENT, OFFICE, OR ORGANIZATION:</h4>'
                entity += '<p>{}</p>'.format(cd['entity'])
                body += entity
            if cd.get('contact_information'):
                contact = '<h4>FOR MORE INFORMATION, CONTACT:</h4>'
                contact += '<p>{}</p>'.format(cd['contact_information'])
                body += contact
            cd['body'] = sanitize(body)
        return cd

    def clean_summary(self):
        summary = sanitize(self.cleaned_data.get('summary'))
        return summary

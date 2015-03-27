from django import forms
from django.conf import settings

from djwailer.core.models import LivewhaleEvents, LivewhaleNews, CATEGORIES

from djtools.fields.time import KungfuTimeField

if settings.DEBUG:
    REQ = {'class': 'required'}
else:
    REQ = {'class': 'required','required': 'required'}

SEND_TO = (
    ('','---------'),
    (False,'[TEST] Communications'),
    (True,'[LIVE] Campus Community'),
)

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

    class Meta:
        model = LivewhaleEvents
        fields = ('title','description','location')

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


class NewsSubmissionForm(forms.ModelForm):
    headline = forms.CharField(max_length=255)
    body = forms.CharField(
        label="Body of Article",
        widget=forms.Textarea
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

    class Meta:
        model = LivewhaleNews
        fields = ('headline','body','summary')


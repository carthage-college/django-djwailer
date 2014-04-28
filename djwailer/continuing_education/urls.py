from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djwailer.continuing_education.views',
    url(
       r'^admissions/information-session/success/$',
       TemplateView.as_view(
           template_name='continuing-education/infosession_success.html'
        ),
        name='cedu_info_session_success'
    ),
    url(
        r'^admissions/information-session/(?P<session_type>[a-zA-Z0-9_-]+)/$',
        'info_session', name="cedu_info_session"
    ),
)

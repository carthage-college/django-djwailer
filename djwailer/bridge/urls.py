from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djwailer.bridge.views',
    url(
        r'^$', RedirectView.as_view(url="/bridge/")
    ),
    url(
        r'^unicode/(?P<oid>\d+)/',
        'unicode_test', name='unicode_test'
    ),
    url(
        r'^(?P<content_type>[\d\w]+)/success/',
        'submission_success', name="submission_success"
    ),
    url(
        r'^(?P<content_type>[\d\w]+)/(?P<oid>\d+)/',
        'submission_form', name='submission_form'
    ),
    url(
        r'^(?P<content_type>[\d\w]+)/',
        'submission_form', name='submission_form'
    ),
)

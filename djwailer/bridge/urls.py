from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from djwailer.bridge import views


urlpatterns = [
    url(
        r'^unicode/(?P<oid>\d+)/',
        views.unicode_test, name='unicode_test'
    ),
    url(
        r'^(?P<content_type>[\d\w]+)/success/',
        views.submission_success, name="submission_success"
    ),
    #url(
    #    r'^(?P<content_type>[\d\w]+)/(?P<oid>\d+)/',
    #    views.submission_form, name='submission_form'
    #),
    url(
        r'^(?P<content_type>[\d\w]+)/',
        views.submission_form, name='submission_form'
    ),
    url(
        r'^$', RedirectView.as_view(url="/bridge/")
    ),
]

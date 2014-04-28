from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djwailer.bridge.views',
    url(r'^$', RedirectView.as_view(url="/bridge/")),
    url(r'^email/$', 'email_test', name='email_test'),
    url(r'^unicode/(?P<oid>\d+)/$', 'unicode_test', name='unicode_test'),
    url(r'^(?P<content_type>[\d\w]+)/success/$', 'submission_success', name="submission_success"),
    url(r'^(?P<content_type>[\d\w]+)/$', 'submission_form', name='submission_form'),
    #url(r'^event/$', 'event_submission_form', name='event_submission_form'),
    #url(r'^event/success/$', TemplateView.as_view(template_name='bridge/event/success.html')),
    #url(r'^news/$', 'news_submission_form', name='news_submission_form'),
    #url(r'^news/success/$', TemplateView.as_view(template_name='bridge/news/success.html')),
)

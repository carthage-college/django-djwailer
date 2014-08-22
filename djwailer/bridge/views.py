# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

from djwailer.bridge.forms import EventSubmissionForm, NewsSubmissionForm
from djwailer.bridge.forms import NewsletterForm
from djwailer.core.models import LivewhaleEvents2Any, TAGS
from djwailer.core.models import LivewhaleEventsCategories2Any
from djwailer.core.models import LivewhaleNews as News
from djwailer.core.models import LivewhaleEvents as Events
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djtools.decorators.auth import superuser_only

import os
import datetime

BCC = settings.MANAGERS
NOW = datetime.date.today()

@login_required
def submission_form(request, content_type, oid=None):
    # try/catch works as 404 detector
    # and GET initialization for forms
    try:
        form = eval(content_type.capitalize() + "SubmissionForm")()
        email_template = "bridge/%s/email.html" % content_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", email_template))
    except:
        raise Http404

    if oid and request.user.is_superuser:
        obj = eval(
            content_type.capitalize()
        ).objects.using("livewhale").get(pk=oid)

    if request.POST:
        form = eval(content_type.capitalize() + "SubmissionForm")(request.POST)
        if form.is_valid():
            usr = request.user
            cd = form.cleaned_data
            data = form.save(commit=False)
            cd["user"] = usr
            data.save(using='livewhale', data=cd)
            subject = "[The Bridge] %s: submitted by %s %s" % (
                content_type.capitalize(), usr.first_name,
                usr.last_name
            )
            # recipients
            if not in_group(usr, "Staff", "Faculty"):
                TO_LIST = settings.BRIDGE_STUDENT
            else:
                TO_LIST = settings.BRIDGE_COMMS

            data.user = usr
            send_mail(
                request, TO_LIST, subject, usr.email,
                "bridge/%s/email.html" % content_type, data, BCC
            )
            return HttpResponseRedirect(
                reverse('submission_success',
                    kwargs={
                        'content_type': content_type,
                    },
                )
            )

    return render_to_response(
        'bridge/%s/form.html' % content_type,
        {"form": form,},
        context_instance=RequestContext(request)
    )

def submission_success(request, content_type):
    return render_to_response(
        "bridge/%s/done.html" % content_type,
        {"content_type": content_type,},
        context_instance=RequestContext(request)
    )

def unicode_test(request,oid):
    funky = News.objects.using('livewhale').get(pk=oid)
    return render_to_response(
        "bridge/unicode.html",
        {"funky":funky,},
        context_instance=RequestContext(request)
    )

def fetch_newsletter(days=4):
    # dates
    #days = 4
    if NOW.strftime("%w") == '2':
        days = 5
    past = NOW - datetime.timedelta(days=days)
    # fetch the news
    news = News.objects.using('livewhale').filter(gid=settings.BRIDGE_GROUP).filter(status=1).filter(date_dt__lte=NOW).filter(is_archived__isnull=True).exclude(date_dt__lte=past)
    for n in news:
        tid = n.tag(jid=True)
        if tid:
            TAGS[tid][1].append(n)
    news = []
    for t in TAGS:
        news.append(TAGS[t])
    return {'news':news}

@superuser_only
def email_test(request):
    if request.GET.get("days"):
        days=int(request.GET.get("days"))
    else:
        days=4
    data = fetch_newsletter(days=days)
    form = NewsletterForm()
    if request.POST:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            arg = "n"
            if cd["send_to"] == "True":
                arg = "y"
            # ok, don't even ask about this #chaputza. bloody livewhale
            os.system("/usr/bin/python /data2/django_projects/django-djwailer/djwailer/bin/bridge_mail.py -s %s" % arg)
            return HttpResponseRedirect(reverse('email_test'))
    t = loader.get_template('bridge/newsletter.html')
    c = RequestContext(request, {'data': data,'form':form,})
    return HttpResponse(t.render(c),
        content_type="text/html; charset=utf8")


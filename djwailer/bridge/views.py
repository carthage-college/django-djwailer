from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from djwailer.bridge.forms import EventSubmissionForm, NewsSubmissionForm
from djwailer.core.models import LivewhaleNews as News
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group

import os

@login_required
def submission_form(request, content_type, oid=None):
    ct = content_type.capitalize()
    obj = None
    # fetch an object or 404
    if oid and request.user.is_superuser: # open up to author at some point
        mod = eval( ct )
        obj = get_object_or_404( mod.objects.using("livewhale"), id=oid )

    # try/catch works as 404 detector
    # and GET initialization for forms
    try:
        form = eval(ct + "SubmissionForm")(instance=obj)
        email_template = "bridge/%s/email.html" % content_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", email_template))
    except:
        raise Http404

    if request.POST:
        form = eval(ct + "SubmissionForm")(request.POST)
        if form.is_valid():
            usr = request.user
            cd = form.cleaned_data
            data = form.save(commit=False)
            cd["user"] = usr
            data.save(using='livewhale', data=cd)
            subject = "[The Bridge] %s: submitted by %s %s" % (
                ct, usr.first_name,
                usr.last_name
            )
            # recipients
            TO_LIST = []
            if not in_group(usr,"carthageStaffStatus","carthageFacultyStatus"):
                TO_LIST = [
                    settings.BRIDGE_STUDENT,settings.BRIDGE_COMMS,usr.email
                ]
            else:
                TO_LIST = [settings.BRIDGE_COMMS,usr.email]

            data.user = usr
            BCC = settings.MANAGERS
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
    # try/catch works as 404 detector
    # and GET initialization for forms
    try:
        template = "bridge/%s/done.html" % content_type
        os.stat(os.path.join(settings.ROOT_DIR, "templates", template))
        return render_to_response(
            template,
            {"content_type": content_type,},
            context_instance=RequestContext(request)
        )
    except:
        raise Http404


def unicode_test(request,oid):
    funky = News.objects.using('livewhale').get(pk=oid)
    return render_to_response(
        "bridge/unicode.html",
        {"funky":funky,},
        context_instance=RequestContext(request)
    )


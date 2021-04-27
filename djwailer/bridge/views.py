# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from djtools.utils.convert import str_to_class
from djtools.utils.mail import send_mail
from djtools.utils.users import in_group
from djwailer.bridge.forms import EventSubmissionForm
from djwailer.bridge.forms import NewsSubmissionForm
from djwailer.core.models import LivewhaleEvents as Event
from djwailer.core.models import LivewhaleNews as News


@login_required
def submission_form(request, content_type, oid=None):
    """Generic submission for form for both News and Events."""
    ct = content_type.capitalize()
    form_name = '{0}SubmissionForm'.format(ct)
    instance = None
    # fetch an object or 404
    if oid and request.user.is_superuser:
        mod = str_to_class('djwailer.core.models', ct)
        instance = get_object_or_404(mod.objects.using('livewhale'), pk=oid)

    email_template = 'bridge/{0}/email.html'.format(content_type)
    # try/catch works as 404 detector
    # and GET initialization for forms
    try:
        os.stat(os.path.join(settings.ROOT_DIR, 'templates', email_template))
    except Exception:
        raise Http404
    form = str_to_class('djwailer.bridge.forms', form_name)(instance=instance)
    if request.POST:
        form = str_to_class('djwailer.bridge.forms', form_name)(request.POST)
        if form.is_valid():
            usr = request.user
            cd = form.cleaned_data
            instance = form.save(commit=False)
            cd['user'] = usr
            instance.save(using='livewhale', data=cd)
            subject = "[The Bridge] {0}: submitted by {1} {2}".format(
                ct,
                usr.first_name,
                usr.last_name,
            )
            # recipients
            student = in_group(usr, 'carthageStudentStatus')
            staff = in_group(usr, 'carthageStaffStatus')
            if settings.DEBUG:
                to_list = [settings.MANAGERS[0][1]]
            else:
                if student and not staff:
                    to_list = [
                        settings.BRIDGE_STUDENT, settings.BRIDGE_COMMS, usr.email,
                    ]
                else:
                    to_list = [settings.BRIDGE_COMMS, usr.email]

            instance.user = usr
            bcc = settings.MANAGERS
            send_mail(
                request,
                to_list,
                subject,
                usr.email,
                'bridge/{0}/email.html'.format(content_type),
                instance,
                bcc,
            )
            return HttpResponseRedirect(
                reverse(
                    'submission_success',
                    kwargs={'content_type': content_type},
                ),
            )

    return render(
        request,
        'bridge/{0}/form.html'.format(content_type),
        {'form': form},
    )


def submission_success(request, content_type):
    """Display the form success page."""
    # try/catch works as 404 detector
    # and GET initialization for forms
    template = 'bridge/{0}/done.html'.format(content_type)
    try:
        os.stat(os.path.join(settings.ROOT_DIR, 'templates', template))
    except Exception:
        raise Http404
    return render(request, template, {'content_type': content_type})


def unicode_test(request, oid):
    """Simple view to test funky characters from the database."""
    funky = News.objects.using('livewhale').get(pk=oid)
    return render(request, 'bridge/unicode.html', {'funky': funky})

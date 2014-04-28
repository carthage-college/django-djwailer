from django.conf import settings
from django.template import RequestContext
from django.utils.timezone import localtime
from django.http import HttpResponseRedirect
from django.utils.dateformat import DateFormat
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse_lazy

from djtools.utils.mail import send_mail
from djwailer.core.models import LivewhaleEvents as Event
from djwailer.continuing_education.forms import InfoSessionForm

BCC = settings.MANAGERS
TO = [settings.SERVER_MAIL]

def info_session(request, session_type):
    if request.method == 'POST':
        form = InfoSessionForm(session_type,request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd["session_type"] = session_type
            # fetch event
            event = Event.objects.using('livewhale').get(pk=cd['event'])
            cd["event"] = event
            # munge datetime
            lc = localtime(event.date_dt)
            df = DateFormat(lc)
            day = df.format('D')
            date = df.format('M d, Y')
            time = df.format('h:ia')
            datetime = "%s. %s at %s" % (day, date, time)
            cd["datetime"] = datetime
            # to
            recipients = settings.CONTINUING_EDUCATION_INFOSESSION_RECIPIENTS
            to = recipients[session_type]
            if settings.DEBUG:
                to = TO
            subject = "Adult Education Information Session Request: "
            subject +="%s on %s" % (session_type, datetime)
            send_mail(
                request, to, subject, cd["email"],
                "continuing-education/infosession.txt", cd, BCC, content="text"
            )
            return HttpResponseRedirect(
                reverse_lazy("cedu_info_session_success")
            )
    else:
        form = InfoSessionForm(session_type)
    return render_to_response(
        'continuing-education/infosession.html',{'form': form,},
        context_instance=RequestContext(request)
    )


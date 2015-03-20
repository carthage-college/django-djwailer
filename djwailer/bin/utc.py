import pytz
import django

django.setup()

from django.conf import settings
from django.utils.timezone import *
from djwailer.core.models import LivewhaleEvents

e = LivewhaleEvents.objects.using("livewhale").get(pk=12183)

print e

print e.date_dt

is_aware(e.date_dt)
is_naive(e.date_dt)

tz = pytz.timezone('UTC')
new = tz.localize(e.date_dt)
print new

pytz.utc.localize(e.date_dt)

now_aware = e.date_dt.replace(tzinfo=pytz.UTC)
print now_aware
is_naive(now_aware)
is_aware(now_aware)
e.date_dt
e.date_dt.replace(tzinfo=settings.TIME_ZONE)
e.date_dt.replace(tzinfo=pytz.CST)
pytz.timezone(settings.TIME_ZONE)
tz= pytz.timezone(settings.TIME_ZONE)
e.date_dt.replace(tzinfo=tz)
e.date_dt


from django.conf import settings

from djwailer.core.models import LivewhaleEvents, LivewhaleNews
import sys, datetime

TAGS = {
    498:['News & Notices',[]],
    499:['Lectures & Presentations',[]],
    500:['Arts & Performances',[]],
    477:['Kudos',[]],
    501:['Faculty News',[]],
    502:['Student News',[]],
    503:['Student Activities',[]],
    504:['Technology',[]],
    544:['Top Bridge Story',[]]
}

days = 6
now = datetime.date.today()
past = now - datetime.timedelta(days=days)
#news = LivewhaleNews.objects.using('livewhale').filter(gid=settings.BRIDGE_GROUP).filter(status=1).filter(date_dt__lte=now).exclude(is_archived="1").exclude(date_dt__lte=past)
news = LivewhaleNews.objects.using('livewhale').filter(gid=settings.BRIDGE_GROUP).filter(status=1).filter(date_dt__lte=now).filter(is_archived__isnull=True).exclude(date_dt__lte=past)
for n in news:
    tid = n.tag(jid=True)
    print "tid = %s " % tid
    if n.is_archived:
        print "archived? %s" % n.is_archived
    if tid:
        TAGS[tid][1].append(n)
news = []
for t in TAGS:
    news.append(TAGS[t])

print news

#print TAGS[498][0]
#print TAGS[498][1]

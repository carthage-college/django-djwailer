# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.utils.timezone import utc
from django.utils.html import escape
from django.utils.encoding import smart_text, force_text

from djtools.utils.database import mysql_db
from djtools.utils.users import in_group
#from djtools.templatetags.text_mungers import convert_smart_quotes

from sanitizer.models import SanitizedCharField, SanitizedTextField

import datetime

CATEGORIES = (
    ('','---------'),
    ('498','News & Notices'),
    ('499','Lectures & Presentations'),
    ('500','Arts & Performances'),
    ('477','Kudos'),
    ('501','Faculty & Staff News'),
    ('502','Student News'),
    ('504','Technology'),
)

SLUGS = {
    498:'news-notices',
    499:'lectures-presentations',
    500:'arts-performances',
    477:'kudos',
    501:'faculty-staff-news',
    502:'students/news',
    504:'technology'
}

TAGS = {
    498:['News & Notices',[]],
    499:['Lectures & Presentations',[]],
    500:['Arts & Performances',[]],
    477:['Kudos',[]],
    501:['Faculty & Staff News',[]],
    502:['Student News',[]],
    504:['Technology',[]],
    544:['Top News Story',[]]
}

BRIDGE_URL = settings.BRIDGE_URL
SERVER_URL = settings.SERVER_URL

SANI_TAGS = [
    'a','b','blockquote','br','em','hr',
    'h1','h2','h3','h4','h5','h6',
    'img','li','ol','p','strong','u','ul'
]

# move somewhere more appropriate
def tags_list():
    li = []
    for c in CATEGORIES:
        if c[0]:
            li.append(c[0])
    li.append(settings.BRIDGE_TOP_STORY_TAG)
    return li

def get_tag(sid,jid):
    try:
        tid  = LivewhaleTags2Any.objects.using('livewhale').filter(id2=sid).filter(id1__in=tags_list())[0].id1
        if jid:
            return tid
        tag  = LivewhaleTags.objects.using('livewhale').get(id=tid)
        slug = SLUGS[tid]
        return '<a href="http://%s%s%s/">%s</a>' % (SERVER_URL,BRIDGE_URL,slug,tag)
    except Exception, e:
        #obj = str('<strong>%s</strong>' % e)
        return ""

class LivewhaleActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    uid = models.IntegerField()
    date = models.DateTimeField()
    message = models.CharField(max_length=1500)
    type = models.CharField(max_length=765)
    flag = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_activity'

class LivewhaleAuthTokens(models.Model):
    token = models.CharField(max_length=96)
    uid = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_auth_tokens'

class LivewhaleBlurbs(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    date = models.CharField(max_length=765)
    date_dt = models.DateTimeField()
    title = models.CharField(max_length=765)
    body = models.TextField(blank=True)
    rank = models.IntegerField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    golive = models.DateTimeField(null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)
    lookup = models.CharField(max_length=765, blank=True)
    is_archived = models.CharField(max_length=3, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_blurbs'

class LivewhaleBlurbsTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    class Meta:
        db_table = u'livewhale_blurbs_types'

class LivewhaleBulletins(models.Model):
    id = models.IntegerField(primary_key=True)
    gids = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765)
    date = models.CharField(max_length=765)
    date_dt = models.DateTimeField()
    body = models.TextField(blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    golive = models.DateTimeField(null=True, blank=True)
    lookup = models.CharField(max_length=765, blank=True)
    status = models.IntegerField()
    class Meta:
        db_table = u'livewhale_bulletins'

class LivewhaleComments(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    type = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    email = models.CharField(max_length=765)
    comment = models.CharField(max_length=30000)
    date = models.DateTimeField()
    status = models.IntegerField()
    class Meta:
        db_table = u'livewhale_comments'

class LivewhaleConfig(models.Model):
    last_report = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=765)
    class Meta:
        db_table = u'livewhale_config'

class LivewhaleCourseCatalog(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765, blank=True)
    crs_no = models.CharField(max_length=384, blank=True)
    abstr = models.TextField(blank=True)
    cat = models.CharField(max_length=24, blank=True)
    dept = models.CharField(max_length=24, blank=True)
    disc = models.CharField(max_length=24, blank=True)
    min_hrs = models.FloatField(null=True, blank=True)
    max_hrs = models.FloatField(null=True, blank=True)
    credits = models.CharField(max_length=24, blank=True)
    sess = models.CharField(max_length=12, blank=True)
    txt = models.CharField(max_length=192, blank=True)
    terms = models.CharField(max_length=384, blank=True)
    firstname = models.CharField(max_length=96, blank=True)
    middlename = models.CharField(max_length=96, blank=True)
    lastname = models.CharField(max_length=192, blank=True)
    suffixname = models.CharField(max_length=96, blank=True)
    fac_id = models.CharField(max_length=48, blank=True)
    email = models.CharField(max_length=384, blank=True)
    instructors = models.CharField(max_length=1536, blank=True)
    core = models.CharField(max_length=12, blank=True)
    class Meta:
        db_table = u'livewhale_course_catalog'

class LivewhaleCustomData(models.Model):
    type = models.CharField(max_length=150, primary_key=True)
    pid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, primary_key=True)
    value = models.CharField(max_length=15000)
    class Meta:
        db_table = u'livewhale_custom_data'

class LivewhaleDbProfiler(models.Model):
    id = models.CharField(max_length=765, primary_key=True)
    query = models.CharField(max_length=15000)
    time1 = models.FloatField(null=True, blank=True)
    time2 = models.FloatField(null=True, blank=True)
    time3 = models.FloatField(null=True, blank=True)
    time4 = models.FloatField(null=True, blank=True)
    time5 = models.FloatField(null=True, blank=True)
    avg_time = models.FloatField()
    last_modified = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_db_profiler'

class LivewhaleEvents(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    eid = models.CharField(max_length=255, blank=True, default="")
    #title = SanitizedCharField(max_length=765, strip=True)
    title = models.CharField(max_length=255)
    date_dt = models.DateTimeField(null=True, blank=True)
    date2_dt = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=255, default=settings.TIME_ZONE)
    is_all_day = models.IntegerField(null=True, blank=True)
    repeats = models.CharField(max_length=1, blank=True)
    # lw15
    repeats_from = models.DateTimeField(null=True, blank=True)
    repeats_until = models.DateTimeField(null=True, blank=True)
    # lw15
    repeats_every = models.IntegerField(null=True, blank=True)
    repeats_by = models.IntegerField(null=True, blank=True)
    repeats_on = models.CharField(max_length=15, blank=True)
    repeats_occurrences = models.IntegerField(null=True, blank=True)
    #summary = SanitizedTextField(blank=True, strip=True)
    summary = models.TextField(blank=True)
    #description = SanitizedTextField(blank=True, allowed_tags=SANI_TAGS, allowed_attributes=['href', 'src'], strip=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    source = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=1)
    location = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(null=True, blank=True, default=settings.BRIDGE_USER)
    lookup = models.CharField(max_length=255, blank=True)
    gallery_id = models.IntegerField(null=True, blank=True)
    has_registration = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    has_invalid_url = models.IntegerField(null=True, blank=True)
    registration_limit = models.IntegerField(null=True, blank=True)
    # lw15
    registration_limit_each = models.IntegerField(null=True, blank=True)
    registration_instructions = models.CharField(max_length=500, blank=True)
    registration_response = models.CharField(max_length=2000, blank=True)
    has_registration_notifications = models.IntegerField(null=True, blank=True)
    registration_notifications_email = models.CharField(max_length=255, blank=True)
    registration_restrict = models.TextField(blank=True)
    registration_owner_email = models.CharField(max_length=255, blank=True)
    has_wait_list = models.IntegerField(null=True, blank=True)
    wait_list_limit = models.IntegerField(null=True, blank=True)
    is_paid = models.IntegerField(null=True, blank=True)
    payment_price = models.CharField(max_length=11, blank=True)
    payment_method = models.IntegerField(null=True, blank=True, default=2)
    cost = models.CharField(max_length=2000, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=1000, blank=True)
    subscription_id = models.CharField(max_length=255, blank=True)
    subscription_pid = models.IntegerField(null=True, blank=True)
    # lw15
    is_canceled = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'livewhale_events'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "http://www.carthage.edu/live/events/%s/" % self.id

    def tag(self, jid=None):
        return get_tag(self.id,jid)

    def save(self, data=None, *args, **kwargs):
        self.title.encode('latin1')
        self.summary.encode('latin1')
        self.description.encode('latin1')
        #self.title.encode('utf8')
        #self.summary.encode('utf8')
        #self.description.encode('utf8')
        #self.title = force_text(self.title.encode('latin1'))
        #self.summary = force_text(self.summary.encode('latin1'))
        #self.description = force_text(self.description.encode('latin1'))
        #self.title = force_text(self.title.encode('utf8'))
        #self.summary = force_text(self.summary.encode('utf8'))
        #self.description = force_text(self.description.encode('utf8'))
        #self.title = force_text(self.title)
        #self.summary = force_text(self.summary)
        #self.description = force_text(self.description)
        #self.title = smart_text(self.title)
        #self.summary = smart_text(self.summary)
        #self.description = smart_text(self.description)
        if data:
            u = data["user"]
            # date munging
            if data['start_time']:
                self.date_dt = datetime.datetime.combine(data['start_date'],data['start_time'])
            else:
                self.date_dt = data['start_date']
            if data['end_time']:
                self.date2_dt = datetime.datetime.combine(data['end_date'],data['end_time'])
            else:
                self.date2_dt = data['end_date']
            # set contact info from request.user
            self.contact_info = '<p>By:&nbsp;<a href="mailto:%s">%s %s</a></p>' % (
                u.email, u.first_name,
                u.last_name
            )
            if in_group(u, "Staff", "Faculty"):
                self.status = 1
            else: # student
                self.status = 0
        # save
        super(LivewhaleEvents, self).save(*args, **kwargs)
        """
        We have to resort to MySQLdb since Django does not support
        composite Foreign Keys
        """
        if data:
            # tag
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    (%s, %s, 'events')
            """ % (data["category"],self.id)
            #cursor = connection.cursor()
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale")
            # category
            sql = """
                INSERT INTO livewhale_events_categories2any
                    (id1, id2, type)
                VALUES
                    (%s, %s, 'events')
            """ % (30,self.id)
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale")

class LivewhaleEvents2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_events2any'

class LivewhaleEvents144(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    eid = models.CharField(max_length=765, blank=True)
    title = models.CharField(max_length=765)
    date = models.CharField(max_length=765)
    date_time = models.CharField(max_length=765, blank=True)
    date_dt = models.DateTimeField(null=True, blank=True)
    date_search = models.DateTimeField()
    date2 = models.CharField(max_length=765, blank=True)
    date2_time = models.CharField(max_length=765, blank=True)
    date2_dt = models.DateTimeField(null=True, blank=True)
    date2_search = models.DateTimeField()
    repeats = models.CharField(max_length=3, blank=True)
    repeats_until = models.CharField(max_length=765, blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=765, blank=True)
    status = models.IntegerField(default=1)
    location = models.CharField(max_length=765, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    lookup = models.CharField(max_length=765, blank=True)
    gallery_id = models.IntegerField(null=True, blank=True)
    search_tags = models.CharField(max_length=1500, blank=True)
    search_categories = models.CharField(max_length=1500, blank=True)
    has_registration = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    has_invalid_url = models.IntegerField(null=True, blank=True)
    registration_limit = models.IntegerField(null=True, blank=True)
    registration_instructions = models.CharField(max_length=1500, blank=True)
    registration_response = models.CharField(max_length=6000, blank=True)
    is_paid = models.IntegerField(null=True, blank=True)
    payment_price = models.CharField(max_length=33, blank=True)
    payment_method = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=3000, blank=True)
    subscription_id = models.CharField(max_length=765, blank=True)
    subscription_pid = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_144'

class LivewhaleEventsCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    is_starred = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_categories'

class LivewhaleEventsCategories2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'livewhale_events_categories2any'

class LivewhaleEventsRegistrations(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    firstname = models.CharField(max_length=765)
    lastname = models.CharField(max_length=765)
    email = models.CharField(max_length=765, blank=True)
    phone = models.CharField(max_length=765, blank=True)
    attending = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=1500, blank=True)
    is_cancelled = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_registrations'

class LivewhaleEventsSubscriptions(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    title = models.CharField(max_length=765)
    url = models.CharField(max_length=1500)
    description = models.CharField(max_length=1500, blank=True)
    last_refreshed = models.DateTimeField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    use_external = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_events_subscriptions'

class LivewhaleFeeds(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=1500, blank=True)
    title = models.CharField(max_length=765, blank=True)
    content = models.TextField(blank=True)
    last_modified = models.DateTimeField()
    type = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_feeds'

class LivewhaleFeedsRateLimits(models.Model):
    name = models.CharField(max_length=765, primary_key=True)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    duration = models.IntegerField()
    total = models.IntegerField()
    max = models.IntegerField()
    class Meta:
        db_table = u'livewhale_feeds_rate_limits'

class LivewhaleFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    date_created = models.DateTimeField()
    summary = models.CharField(max_length=765, blank=True)
    type = models.CharField(max_length=765)
    filename = models.CharField(max_length=765, blank=True)
    extension = models.CharField(max_length=765, blank=True)
    status = models.CharField(max_length=3)
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_files'

class LivewhaleFiles2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_files2any'

class LivewhaleForms(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    date_created = models.DateTimeField()
    status = models.IntegerField()
    intro = models.TextField(blank=True)
    thanks = models.TextField(blank=True)
    action = models.IntegerField()
    email = models.CharField(max_length=765, blank=True)
    structure = models.TextField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    is_secure = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=765, blank=True)
    views = models.IntegerField(null=True, blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    use_captcha = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_forms'

class LivewhaleForms2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_forms2any'

class LivewhaleFormsData(models.Model):
    id = models.IntegerField(primary_key=True)
    fid = models.IntegerField()
    data = models.TextField()
    date_dt = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_forms_data'

class LivewhaleGalleries(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    description = models.TextField(blank=True)
    rank = models.IntegerField()
    lookup = models.CharField(max_length=765, blank=True)
    status = models.IntegerField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=765, blank=True)
    views = models.IntegerField(null=True, blank=True)
    date = models.CharField(max_length=765)
    date_dt = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_galleries'

class LivewhaleGalleries2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_galleries2any'

class LivewhaleGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    fullname = models.CharField(max_length=765)
    fullname_public = models.CharField(max_length=765, blank=True)
    directory = models.CharField(max_length=765, blank=True)
    modules = models.CharField(max_length=1500, blank=True)
    timezone = models.CharField(max_length=765, blank=True)
    default_template = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_groups'

class LivewhaleGroupsSettings(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, primary_key=True)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'livewhale_groups_settings'

class LivewhaleHosts(models.Model):
    host = models.CharField(max_length=150, primary_key=True)
    last_detected = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_hosts'

class LivewhaleImages(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=765)
    filename = models.CharField(max_length=765, blank=True)
    extension = models.CharField(max_length=765, blank=True)
    keywords = models.CharField(max_length=1500, blank=True)
    credit = models.CharField(max_length=3000, blank=True)
    caption = models.CharField(max_length=3000, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    lookup = models.CharField(max_length=765, blank=True)
    date = models.CharField(max_length=765)
    date_dt = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_images'

class LivewhaleImages2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    caption = models.CharField(max_length=3000, blank=True)
    is_thumb = models.IntegerField(null=True, blank=True)
    only_thumb = models.IntegerField(null=True, blank=True)
    full_crop = models.IntegerField(null=True, blank=True)
    full_src_region = models.CharField(max_length=765, blank=True)
    thumb_crop = models.IntegerField(null=True, blank=True)
    thumb_src_region = models.CharField(max_length=765, blank=True)
    position = models.CharField(max_length=765)
    type = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'livewhale_images2any'

class LivewhaleMessages(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    message = models.CharField(max_length=1500)
    type = models.CharField(max_length=765, blank=True)
    pid = models.IntegerField(null=True, blank=True)
    module = models.CharField(max_length=765, blank=True)
    date_created = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_messages'

class LivewhaleMissions(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=1500)
    description = models.TextField()
    status = models.IntegerField()
    golive = models.DateTimeField(null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)
    tag = models.CharField(max_length=765, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    class Meta:
        db_table = u'livewhale_missions'

class LivewhaleModules(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, unique=True)
    revision = models.FloatField()
    class Meta:
        db_table = u'livewhale_modules'

class LivewhaleTags(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    is_starred = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'livewhale_tags'

    def __unicode__(self):
        return self.title

class LivewhaleTags2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)

    class Meta:
        db_table = u'livewhale_tags2any'

class LivewhaleNews(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=1500, blank=True, default=None)
    parent = models.IntegerField(null=True, blank=True)
    #headline = SanitizedCharField(max_length=765, strip=True)
    headline = models.CharField(max_length=255)
    #summary = SanitizedTextField(blank=True, strip=True)
    summary = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    #body = SanitizedTextField(blank=True, allowed_tags=SANI_TAGS, allowed_attributes=['href', 'src'], strip=True)
    body = models.TextField(blank=True)
    contact_info = models.CharField(max_length=1000, blank=True)
    rank = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(null=True, blank=True, default=settings.BRIDGE_USER)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=255, blank=True, default=None)
    is_starred = models.IntegerField(null=True, blank=True)
    golive = models.DateTimeField(null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)
    lookup = models.CharField(max_length=255, blank=True, default=None)
    gallery_id = models.IntegerField(null=True, blank=True)
    is_archived = models.CharField(max_length=1, blank=True,default=None)
    has_invalid_url = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'livewhale_news'

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return "http://www.carthage.edu/live/news/%s/" % self.id

    def tag(self, jid=None):
        return get_tag(self.id,jid)

    def save(self, data=None, *args, **kwargs):
        #import re
        #self.headline = convert_smart_quotes(self.headline)
        #self.summary = convert_smart_quotes(self.summary)
        #self.body = convert_smart_quotes(self.body)
        #self.headline.encode('latin1')
        #self.summary.encode('latin1')
        #self.body.encode('latin1')
        #self.headline = self.headline.encode('latin1').replace('“','"').replace('”','"')
        #self.summary = self.summary.encode('latin1').replace('“','"').replace('”','"')
        #self.body = self.body.encode('latin1').replace('“','"').replace('”','"')
        #self.headline = self.headline.encode('latin1')
        #self.summary = self.summary.encode('latin1')
        #self.body = self.body.encode('latin1')
        #h = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"',self.headline.encode('utf-8'))
        #s = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"',self.summary.encode('utf-8'))
        #b = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"',self.body.encode('utf-8'))
        #h = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','&quot;',self.headline.encode('utf-8'))
        #s = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','&quot;',self.summary.encode('utf-8'))
        #b = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','&quot;',self.body.encode('utf-8'))
        #self.headline = h
        #self.summary = s
        #self.body = b
        #self.headline = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"', h)
        #self.summary =  re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"', s)
        #self.body = re.sub(u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]','"', b)
        #self.headline = self.headline.replace(u'“','"').replace(u'”','"')
        #self.summary = self.summary.replace(u'“','"').replace(u'”','"')
        #self.body = self.body.replace(u'“','"').replace(u'”','"')
        #self.headline = h.replace(u'“','"').replace(u'”','"')
        #self.summary = s.replace(u'“','"').replace(u'”','"')
        #self.body = b.replace(u'“','"').replace(u'”','"')
        #headline = self.headline
        #summary = self.summary
        #body = self.body
        #self.headline = " "
        #self.summary = " "
        #self.body = " "
        # set contact info from request.user
        if data:
            u = data["user"]
            self.contact_info = '<p><a href="mailto:%s">%s %s</a></p>' % (
                u.email, u.first_name, u.last_name
            )
            #from django.utils import timezone
            #timezone.deactivate()
            #timezone.activate('US/Central')
            #timezone.activate('America/Chicago')
            #self.date_dt = timezone.now()
            self.date_dt = datetime.datetime.combine(datetime.date.today(),datetime.time())
            self.date    = self.date_dt.strftime("%m/%d/%Y")
            if in_group(u, "Staff", "Faculty"):
                self.status = 1
            else: # student
                self.status = 0
        # save
        super(LivewhaleNews, self).save(*args, **kwargs)

        """
        We have to resort to MySQLdb because:
            a) livewhale's database is fucked up
            b) Django does not support composite Foreign Keys
        """
        if data:
            cursor = connection.cursor()
            # create the object
            '''
            sql = """
                UPDATE
                    livewhale_news
                SET
                    headline='%s',summary='%s',body='%s'
                WHERE id = %s
            """ % (headline,summary,body,self.id)
            mysql_db(sql,db="livewhale")
            '''

            """
            import MySQLdb
            hs = "localhost"
            db = "livewhale_staging_2"
            conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,use_unicode=True,charset="utf8")
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db)
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,use_unicode=True,charset="ascii")
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,charset="ascii")
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,use_unicode=True)
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,use_unicode=True,charset="latin1")
            #conn  = MySQLdb.connect(host=hs,user=us,passwd=ps,db=db,charset="utf8")

            curr = conn.cursor()
            curr.execute(sql)
            conn.commit()
            curr.close ()
            conn.close ()
            """
            # tag it
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    (%s, %s, 'news')
            """ % (data["category"],self.id)
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale")

class LivewhaleNews2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_news2any'

class LivewhalePages(models.Model):
    id = models.IntegerField(unique=True)
    gids = models.CharField(max_length=3000, blank=True)
    uids = models.CharField(max_length=3000, blank=True)
    path = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    depth = models.IntegerField()
    title = models.CharField(max_length=765, blank=True)
    short_title = models.CharField(max_length=765, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField(null=True, blank=True)
    content = models.TextField()
    elements = models.TextField(blank=True)
    note = models.CharField(max_length=765, blank=True)
    is_editing_ts = models.IntegerField(null=True, blank=True)
    is_editing_user = models.IntegerField(null=True, blank=True)
    is_template = models.IntegerField(null=True, blank=True)
    host = models.CharField(max_length=150, primary_key=True)
    ga_year = models.IntegerField(null=True, blank=True)
    ga_month = models.IntegerField(null=True, blank=True)
    ga_week = models.IntegerField(null=True, blank=True)
    ga_keywords = models.CharField(max_length=1500, blank=True)
    schedule = models.CharField(max_length=3000, blank=True)
    schedule_expires = models.DateTimeField(null=True, blank=True)
    schedule_expires_type = models.IntegerField(null=True, blank=True)
    schedule_to_type = models.IntegerField(null=True, blank=True)
    schedule_to_email = models.CharField(max_length=765, blank=True)
    diff = models.TextField(blank=True)
    subscriptions = models.TextField(blank=True)
    subscriptions_date = models.DateTimeField(null=True, blank=True)
    total_errors = models.IntegerField(null=True, blank=True)
    is_draft = models.IntegerField(null=True, blank=True)
    is_draft_closure = models.IntegerField(null=True, blank=True)
    accessibility_score = models.IntegerField(null=True, blank=True)
    accessibility_report = models.CharField(max_length=15000, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    thash = models.CharField(max_length=96, blank=True)
    description = models.CharField(max_length=1500, blank=True)
    keywords = models.CharField(max_length=1500, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    is_qa = models.IntegerField(null=True, blank=True)
    has_editable_regions = models.IntegerField(null=True, blank=True)
    is_details_template = models.IntegerField(null=True, blank=True)
    is_no_editing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_pages'

class LivewhalePages2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_pages2any'

class LivewhalePagesAuthorization(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    path = models.CharField(max_length=765)
    host = models.CharField(max_length=150)
    class Meta:
        db_table = u'livewhale_pages_authorization'

class LivewhalePagesNavs(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    title = models.CharField(max_length=765)
    host = models.CharField(max_length=150)
    is_main = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_pages_navs'

class LivewhalePagesNavsItems(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    depth = models.IntegerField(null=True, blank=True)
    pgid = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=12)
    status = models.IntegerField()
    title = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_pages_navs_items'

class LivewhalePagesNotes(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    uid = models.IntegerField()
    date = models.DateTimeField()
    type = models.IntegerField()
    note = models.CharField(max_length=1500)
    class Meta:
        db_table = u'livewhale_pages_notes'

class LivewhalePagesRevisions(models.Model):
    id = models.IntegerField(unique=True)
    gids = models.CharField(max_length=3000, blank=True)
    uids = models.CharField(max_length=3000, blank=True)
    pid = models.IntegerField()
    path = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    depth = models.IntegerField()
    title = models.CharField(max_length=765, blank=True)
    short_title = models.CharField(max_length=765, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField(null=True, blank=True)
    content = models.TextField()
    elements = models.TextField()
    note = models.CharField(max_length=765, blank=True)
    host = models.CharField(max_length=150, primary_key=True)
    ga_year = models.IntegerField(null=True, blank=True)
    ga_month = models.IntegerField(null=True, blank=True)
    ga_week = models.IntegerField(null=True, blank=True)
    ga_keywords = models.CharField(max_length=1500, blank=True)
    schedule = models.CharField(max_length=3000, blank=True)
    schedule_expires = models.DateTimeField(null=True, blank=True)
    schedule_expires_type = models.IntegerField(null=True, blank=True)
    schedule_to_type = models.IntegerField(null=True, blank=True)
    schedule_to_email = models.CharField(max_length=765, blank=True)
    diff = models.TextField(blank=True)
    subscriptions = models.TextField(blank=True)
    subscriptions_date = models.DateTimeField(null=True, blank=True)
    total_errors = models.IntegerField(null=True, blank=True)
    is_draft = models.IntegerField(null=True, blank=True)
    is_draft_closure = models.IntegerField(null=True, blank=True)
    accessibility_score = models.IntegerField(null=True, blank=True)
    accessibility_report = models.CharField(max_length=15000, blank=True)
    tid = models.IntegerField(null=True, blank=True)
    thash = models.CharField(max_length=96, blank=True)
    description = models.CharField(max_length=1500, blank=True)
    keywords = models.CharField(max_length=1500, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    is_qa = models.IntegerField(null=True, blank=True)
    has_editable_regions = models.IntegerField(null=True, blank=True)
    is_details_template = models.IntegerField(null=True, blank=True)
    is_no_editing = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_pages_revisions'

class LivewhalePagesTemplates(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    uid = models.IntegerField(null=True, blank=True)
    path = models.CharField(max_length=765)
    host = models.CharField(max_length=150)
    class Meta:
        db_table = u'livewhale_pages_templates'

class LivewhalePaymentsOrders(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    gateway = models.CharField(max_length=765)
    gateway_response = models.CharField(max_length=30000, blank=True)
    order_quantity = models.IntegerField()
    order_total = models.CharField(max_length=33)
    order_date = models.DateTimeField()
    product_description = models.CharField(max_length=765)
    product_type = models.CharField(max_length=765, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    customer_first_name = models.CharField(max_length=765)
    customer_last_name = models.CharField(max_length=765)
    customer_email = models.CharField(max_length=765)
    customer_phone = models.CharField(max_length=765)
    customer_address = models.CharField(max_length=765, blank=True)
    customer_city = models.CharField(max_length=765, blank=True)
    customer_state = models.CharField(max_length=765, blank=True)
    customer_zip = models.CharField(max_length=765, blank=True)
    customer_country = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_payments_orders'

class LivewhalePaymentsSettings(models.Model):
    gid = models.IntegerField(primary_key=True)
    gateway = models.CharField(max_length=765, blank=True)
    name = models.CharField(max_length=765, primary_key=True)
    value = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_payments_settings'

class LivewhalePlaces(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    latitude = models.FloatField()
    longitude = models.FloatField()
    keywords = models.CharField(max_length=1500, blank=True)
    is_preset = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    thumb = models.CharField(max_length=765, blank=True)
    requires_reservation = models.IntegerField(null=True, blank=True)
    reservation_instructions = models.CharField(max_length=1500, blank=True)
    class Meta:
        db_table = u'livewhale_places'

class LivewhalePlaces2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    class Meta:
        db_table = u'livewhale_places2any'

class LivewhaleProfiles(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    tid = models.IntegerField(null=True, blank=True)
    suggested = models.CharField(max_length=1500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    firstname = models.CharField(max_length=765)
    middlename = models.CharField(max_length=765, blank=True)
    lastname = models.CharField(max_length=765)
    description = models.TextField(blank=True)
    status = models.IntegerField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    is_starred = models.IntegerField(null=True, blank=True)
    lookup = models.CharField(max_length=765, blank=True)
    gallery_id = models.IntegerField(null=True, blank=True)
    is_shared = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=1500, blank=True)
    source = models.CharField(max_length=765, blank=True)
    views = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=3000, blank=True)
    username = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_profiles'

class LivewhaleProfiles2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_profiles2any'

class LivewhaleProfilesFields(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    fid = models.IntegerField()
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'livewhale_profiles_fields'

class LivewhaleProfilesTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_profiles_types'

class LivewhaleProfilesTypesFields(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    title = models.CharField(max_length=765)
    type = models.CharField(max_length=765)
    position = models.IntegerField()
    allow_in_linked = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'livewhale_profiles_types_fields'

class LivewhalePublicSubmissions(models.Model):
    id = models.IntegerField(primary_key=True)
    submitter_id = models.IntegerField()
    submission_id = models.IntegerField()
    submission_type = models.CharField(max_length=765)
    submission_title = models.CharField(max_length=765)
    submission_date = models.DateTimeField()
    mission_id = models.IntegerField(null=True, blank=True)
    mission_title = models.CharField(max_length=1500, blank=True)
    has_copies = models.IntegerField(null=True, blank=True)
    from_livewhale_reporter = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_public_submissions'

class LivewhalePublicSubmitters(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765)
    email = models.CharField(max_length=765)
    class Meta:
        db_table = u'livewhale_public_submitters'

class LivewhaleRedirects(models.Model):
    id = models.IntegerField(primary_key=True)
    host = models.CharField(max_length=150)
    url = models.CharField(max_length=765)
    destination = models.CharField(max_length=765)
    last_used = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_redirects'

class LivewhaleRevisions(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    uid = models.IntegerField()
    type = models.CharField(max_length=765)
    date = models.DateTimeField()
    revision = models.TextField()
    search = models.TextField(blank=True)
    class Meta:
        db_table = u'livewhale_revisions'

class LivewhaleScheduler(models.Model):
    name = models.CharField(max_length=765, primary_key=True)
    exec_field = models.CharField(max_length=765, db_column='exec') # Field renamed because it was a Python reserved word.
    next_execution = models.DateTimeField()
    frequency = models.IntegerField()
    env = models.CharField(max_length=42)
    class Meta:
        db_table = u'livewhale_scheduler'

class LivewhaleSearch(models.Model):
    type = models.CharField(max_length=765, primary_key=True)
    pid = models.CharField(max_length=150, primary_key=True)
    title = models.CharField(max_length=765)
    high_content = models.CharField(max_length=3000, blank=True)
    medium_content = models.CharField(max_length=15000, blank=True)
    low_content = models.TextField(blank=True)
    url = models.CharField(max_length=1500, blank=True)
    hash = models.CharField(max_length=765, blank=True)
    last_modified = models.DateTimeField()
    class Meta:
        db_table = u'livewhale_search'

class LivewhaleTrash(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    pid = models.IntegerField()
    title = models.CharField(max_length=765)
    type = models.CharField(max_length=765)
    date_deleted = models.DateTimeField()
    content = models.TextField(blank=True)
    content_file = models.TextField(blank=True)
    class Meta:
        db_table = u'livewhale_trash'

class LivewhaleUrls(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765)
    url = models.CharField(max_length=1500, blank=True)
    class Meta:
        db_table = u'livewhale_urls'

class LivewhaleUrls2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()
    class Meta:
        db_table = u'livewhale_urls2any'

class LivewhaleUrlsShortened(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=3000)
    date_created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_urls_shortened'

class LivewhaleUsers(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField()
    username = models.CharField(max_length=765, unique=True)
    password = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765, blank=True)
    firstname = models.CharField(max_length=765, blank=True)
    lastname = models.CharField(max_length=765, blank=True)
    name = models.CharField(max_length=765, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_access = models.DateTimeField(null=True, blank=True)
    authorized_modules = models.CharField(max_length=1500, blank=True)
    is_admin = models.CharField(max_length=3, blank=True)
    is_reporter = models.CharField(max_length=3, blank=True)
    use_email = models.CharField(max_length=3, blank=True)
    switch_groups = models.CharField(max_length=15000, blank=True)
    total_errors = models.IntegerField(null=True, blank=True)
    tag = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_users'

class LivewhaleUsersSettings(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, primary_key=True)
    value = models.CharField(max_length=765)
    class Meta:
        db_table = u'livewhale_users_settings'

class LivewhaleWidgetCache(models.Model):
    host = models.CharField(max_length=150)
    ip = models.CharField(max_length=135)
    page = models.CharField(max_length=765)
    query = models.CharField(max_length=765, blank=True)
    type = models.CharField(max_length=765)
    gids = models.CharField(max_length=765, blank=True)
    tags = models.CharField(max_length=765, blank=True)
    hash = models.CharField(max_length=150, primary_key=True)
    last_modified = models.DateTimeField()
    expires = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True)
    content_vars = models.TextField(blank=True)
    name = models.CharField(max_length=765, blank=True)
    id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'livewhale_widget_cache'

class LivewhaleWidgets(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=765)
    description = models.CharField(max_length=1500, blank=True)
    name = models.CharField(max_length=765)
    type = models.CharField(max_length=765)
    args = models.CharField(max_length=30000)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    class Meta:
        db_table = u'livewhale_widgets'


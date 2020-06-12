# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, connection
from django.utils.html import strip_tags

from djtools.utils.database import mysql_db
from djtools.utils.users import in_group

import datetime

CATEGORIES = (
    ('', '---------'),
    ('498', 'News & Notices'),
    ('499', 'Lectures & Presentations'),
    ('1498', 'Dear Lake, We Miss You'),
    ('500', 'Arts & Performances'),
    ('477', 'Kudos'),
    ('501', 'Faculty & Staff News'),
    ('502', 'Student News'),
    ('504', 'Library & Technology'),
)

SLUGS = {
    498:'news-notices',
    499:'lectures-presentations',
    500:'arts-performances',
    477:'kudos',
    501:'faculty-staff-news',
    502:'students/news',
    504:'technology',
}

BRIDGE_URL = settings.BRIDGE_URL
SERVER_URL = settings.SERVER_URL
SSL = {
    'cert': '/d2/www/certs/mysql/titan.carthage.edu/client-cert.pem',
    'key': '/d2/www/certs/mysql/titan.carthage.edu/client-key.pem'
}

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
        tid  = LivewhaleTags2Any.objects.using(
            'livewhale'
        ).filter(id2=sid).filter(type="news").filter(id1__in=tags_list())[0].id1
        return tid
        #tag  = LivewhaleTags.objects.using('livewhale').get(id=tid)
        #slug = SLUGS[tid]
        #return '<a href="http://{}{}{}/">{}</a>'.format(
        #    SERVER_URL,BRIDGE_URL,slug,tag
        #)
    except Exception, e:
        #obj = str('<strong>{}</strong>'.format(e))
        return ""

class LivewhaleActivity(models.Model):
    gid = models.IntegerField()
    uid = models.IntegerField()
    date = models.DateTimeField()
    message = models.CharField(max_length=2000)
    type = models.CharField(max_length=255)
    flag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_activity'


class LivewhaleAuthTokens(models.Model):
    token = models.CharField(max_length=50)
    uid = models.IntegerField(primary_key=True)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_auth_tokens'


class LivewhaleBlogs(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_restricted = models.IntegerField(blank=True, null=True)
    has_moderation = models.IntegerField(blank=True, null=True)
    moderators = models.CharField(max_length=500, blank=True, null=True)
    has_contributors = models.IntegerField(blank=True, null=True)
    contributors = models.CharField(max_length=500, blank=True, null=True)
    disqus_shortname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blogs'


class LivewhaleBlogsFields(models.Model):
    pid = models.IntegerField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    position = models.IntegerField()
    allow_in_linked = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    instructional_text = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.IntegerField(blank=True, null=True)
    field_options = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blogs_fields'


class LivewhaleBlogsPosts(models.Model):
    gid = models.IntegerField()
    bid = models.IntegerField(blank=True, null=True)
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    post = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    gallery_id = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField()
    has_invalid_url = models.IntegerField(blank=True, null=True)
    golive = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blogs_posts'


class LivewhaleBlogsPosts2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_blogs_posts2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleBlogsPostsFields(models.Model):
    pid = models.IntegerField()
    fid = models.IntegerField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blogs_posts_fields'


class LivewhaleBlurbs(models.Model):
    gid = models.IntegerField()
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    tid = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    rank = models.IntegerField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    golive = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blurbs'


class LivewhaleBlurbsTypes(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    auto_authorize = models.IntegerField(blank=True, null=True)
    has_details_template = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_blurbs_types'


class LivewhaleBulletins(models.Model):
    gids = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    body = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    golive = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_bulletins'


class LivewhaleConfig(models.Model):
    last_report = models.DateTimeField(blank=True, null=True)
    version = models.CharField(primary_key=True, max_length=255)
    uuid = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_config'


class LivewhaleCourseCatalog(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    crs_no = models.CharField(max_length=128, blank=True, null=True)
    abstr = models.TextField(blank=True, null=True)
    cat = models.CharField(max_length=8, blank=True, null=True)
    dept = models.CharField(max_length=8, blank=True, null=True)
    disc = models.CharField(max_length=8, blank=True, null=True)
    min_hrs = models.FloatField(blank=True, null=True)
    max_hrs = models.FloatField(blank=True, null=True)
    credits = models.CharField(max_length=8, blank=True, null=True)
    sess = models.CharField(max_length=4, blank=True, null=True)
    txt = models.CharField(max_length=64, blank=True, null=True)
    terms = models.CharField(max_length=128, blank=True, null=True)
    firstname = models.CharField(max_length=32, blank=True, null=True)
    middlename = models.CharField(max_length=32, blank=True, null=True)
    lastname = models.CharField(max_length=64, blank=True, null=True)
    suffixname = models.CharField(max_length=32, blank=True, null=True)
    fac_id = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    instructors = models.CharField(max_length=512, blank=True, null=True)
    core = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'livewhale_course_catalog'


class LivewhaleCustomData(models.Model):
    type = models.CharField(primary_key=True, max_length=50)
    pid = models.IntegerField()
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=5000)
    is_public = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_custom_data'
        unique_together = (('type', 'pid', 'name'),)


class LivewhaleDbProfiler(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    query = models.CharField(max_length=10000)
    time1 = models.FloatField(blank=True, null=True)
    time2 = models.FloatField(blank=True, null=True)
    time3 = models.FloatField(blank=True, null=True)
    time4 = models.FloatField(blank=True, null=True)
    time5 = models.FloatField(blank=True, null=True)
    avg_time = models.FloatField()
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_db_profiler'


class LivewhaleDrafts(models.Model):
    editor = models.CharField(primary_key=True, max_length=50)
    data_type = models.CharField(max_length=30)
    vary_by = models.CharField(max_length=50)
    uid = models.IntegerField()
    pid = models.IntegerField()
    data = models.TextField()
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_drafts'
        unique_together = (('editor', 'vary_by', 'uid', 'pid'),)


class LivewhaleEvents(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    eid = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    date_dt = models.DateTimeField(blank=True, null=True)
    date2_dt = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=255, default=settings.TIME_ZONE)
    is_all_day = models.IntegerField(blank=True, null=True)
    is_multi_day = models.IntegerField(blank=True, null=True)
    repeats = models.CharField(max_length=1, blank=True, null=True)
    repeats_from = models.DateTimeField(blank=True, null=True)
    repeats_until = models.DateTimeField(blank=True, null=True)
    repeats_every = models.IntegerField(blank=True, null=True)
    repeats_by = models.IntegerField(blank=True, null=True)
    repeats_on = models.CharField(max_length=15, blank=True, null=True)
    repeats_occurrences = models.IntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(
        null=True, blank=True, default=settings.BRIDGE_USER
    )
    gallery_id = models.IntegerField(blank=True, null=True)
    has_registration = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    has_invalid_url = models.IntegerField(blank=True, null=True)
    registration_limit = models.IntegerField(blank=True, null=True)
    registration_limit_each = models.IntegerField(blank=True, null=True)
    registration_instructions = models.CharField(max_length=500, blank=True, null=True)
    registration_response = models.CharField(max_length=2000, blank=True, null=True)
    has_registration_notifications = models.IntegerField(blank=True, null=True)
    registration_notifications_email = models.CharField(max_length=255, blank=True, null=True)
    registration_restrict = models.TextField(blank=True, null=True)
    registration_owner_email = models.CharField(max_length=255, blank=True, null=True)
    registration_open = models.DateTimeField(blank=True, null=True)
    registration_close = models.DateTimeField(blank=True, null=True)
    has_wait_list = models.IntegerField(blank=True, null=True)
    wait_list_limit = models.IntegerField(blank=True, null=True)
    is_paid = models.IntegerField(blank=True, null=True)
    payment_price = models.CharField(max_length=11, blank=True, null=True)
    payment_method = models.IntegerField(blank=True, null=True)
    cost_type = models.IntegerField(blank=True, null=True)
    cost = models.CharField(max_length=2000, blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    contact_info = models.CharField(max_length=1000, blank=True, null=True)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscription_pid = models.IntegerField(blank=True, null=True)
    is_canceled = models.IntegerField(blank=True, null=True)
    style = models.CharField(max_length=10, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    has_customized_description = models.IntegerField(blank=True, null=True)
    has_customized_location = models.IntegerField(blank=True, null=True)
    has_customized_contact_info = models.IntegerField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_events'

    def get_absolute_url(self):
        return "https://www.carthage.edu/live/events/{}/".format(self.id)

    def save(self, data=None, *args, **kwargs):
        self.title = strip_tags(self.title).encode('utf8')
        self.summary = strip_tags(self.summary).encode('utf8')
        self.description = self.description.encode('utf8')
        self.location = strip_tags(self.location).encode('utf8')

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
            self.contact_info = '''
                <p>By:&nbsp;<a href="mailto:{}">{} {}</a></p>
            '''.format(u.email, u.first_name, u.last_name)

            if in_group(u, "carthageStaffStatus", "carthageFacultyStatus"):
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
                    ({}, {}, 'events')
            """.format(data["category"],self.id)
            #cursor = connection.cursor()
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale",ssl=SSL)
            # category
            sql = """
                INSERT INTO livewhale_events_categories2any
                    (id1, id2, type)
                VALUES
                    ({}, {}, 'events')
            """.format(30,self.id)
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale",ssl=SSL)


class LivewhaleEvents2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_events2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleEventsCategories(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    is_starred = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_events_categories'


class LivewhaleEventsCategories2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_events_categories2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleEventsRegistrations(models.Model):
    pid = models.IntegerField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    attending = models.IntegerField(blank=True, null=True)
    comments_by_registrant = models.CharField(max_length=500, blank=True, null=True)
    comments_by_editor = models.CharField(max_length=500, blank=True, null=True)
    is_cancelled = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    is_waitlisted = models.IntegerField(blank=True, null=True)
    custom_fields = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_events_registrations'


class LivewhaleEventsSubscriptions(models.Model):
    gid = models.IntegerField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True, null=True)
    last_refreshed = models.DateTimeField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    use_external = models.IntegerField(blank=True, null=True)
    gallery_id = models.IntegerField(blank=True, null=True)
    has_registration = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    registration_limit = models.IntegerField(blank=True, null=True)
    registration_limit_each = models.IntegerField(blank=True, null=True)
    registration_instructions = models.CharField(max_length=500, blank=True, null=True)
    registration_response = models.CharField(max_length=2000, blank=True, null=True)
    has_registration_notifications = models.IntegerField(blank=True, null=True)
    registration_notifications_email = models.CharField(max_length=255, blank=True, null=True)
    registration_restrict = models.TextField(blank=True, null=True)
    registration_owner_email = models.CharField(max_length=255, blank=True, null=True)
    has_wait_list = models.IntegerField(blank=True, null=True)
    wait_list_limit = models.IntegerField(blank=True, null=True)
    is_paid = models.IntegerField(blank=True, null=True)
    payment_price = models.CharField(max_length=11, blank=True, null=True)
    payment_method = models.IntegerField(blank=True, null=True)
    cost_type = models.IntegerField(blank=True, null=True)
    cost = models.CharField(max_length=2000, blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    contact_info = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_events_subscriptions'


class LivewhaleFeeds(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField()
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_feeds'


class LivewhaleFeedsRateLimits(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    duration = models.IntegerField()
    total = models.IntegerField()
    max = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_feeds_rate_limits'


class LivewhaleFiles(models.Model):
    gid = models.IntegerField()
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    summary = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=1)
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)
    last_accessed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_files'


class LivewhaleFiles2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_files2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleForms(models.Model):
    gid = models.IntegerField()
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    intro = models.TextField(blank=True, null=True)
    thanks = models.TextField(blank=True, null=True)
    action = models.IntegerField()
    email = models.CharField(max_length=255, blank=True, null=True)
    structure = models.TextField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    use_captcha = models.IntegerField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)
    response = models.IntegerField(blank=True, null=True)
    response_url = models.CharField(max_length=255, blank=True, null=True)
    has_confirmations = models.IntegerField(blank=True, null=True)
    reply_to = models.CharField(max_length=255, blank=True, null=True)
    confirmation_response = models.CharField(max_length=2000, blank=True, null=True)
    from_primary_email = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_forms'


class LivewhaleForms2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_forms2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleFormsData(models.Model):
    fid = models.IntegerField()
    data = models.TextField()
    date_dt = models.DateTimeField()
    rsvp_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_forms_data'


class LivewhaleGalleries(models.Model):
    gid = models.IntegerField()
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rank = models.IntegerField()
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    is_archived = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_galleries'


class LivewhaleGalleries2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_galleries2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleGroups(models.Model):
    fullname = models.CharField(max_length=255)
    fullname_public = models.CharField(max_length=255, blank=True, null=True)
    directory = models.CharField(max_length=255, blank=True, null=True)
    modules = models.CharField(max_length=500, blank=True, null=True)
    timezone = models.CharField(max_length=255, blank=True, null=True)
    default_template = models.CharField(max_length=255, blank=True, null=True)
    twitter_name = models.CharField(max_length=30, blank=True, null=True)
    facebook_name = models.CharField(max_length=30, blank=True, null=True)
    instagram_name = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    woeid = models.CharField(max_length=30, blank=True, null=True)
    use_gid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_groups'


class LivewhaleGroupsSettings(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_groups_settings'
        unique_together = (('gid', 'name'),)


class LivewhaleHosts(models.Model):
    host = models.CharField(primary_key=True, max_length=50)
    last_detected = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_hosts'


class LivewhaleImages(models.Model):
    gid = models.IntegerField()
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField(max_length=1000, blank=True, null=True)
    caption = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField()
    collection_id = models.IntegerField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)
    last_accessed = models.DateTimeField()
    is_decoration = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_images'


class LivewhaleImages2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    caption = models.CharField(max_length=1000, blank=True, null=True)
    is_thumb = models.IntegerField(blank=True, null=True)
    only_thumb = models.IntegerField(blank=True, null=True)
    full_crop = models.IntegerField(blank=True, null=True)
    full_src_region = models.CharField(max_length=255, blank=True, null=True)
    thumb_crop = models.IntegerField(blank=True, null=True)
    thumb_src_region = models.CharField(max_length=255, blank=True, null=True)
    is_decoration = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_images2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleImagesCollections(models.Model):
    gid = models.IntegerField()
    title = models.CharField(max_length=30)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_images_collections'


class LivewhaleLanguagesFields(models.Model):
    pid = models.IntegerField()
    type = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'livewhale_languages_fields'


class LivewhaleMessages(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=500)
    type = models.CharField(max_length=255, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_messages'


class LivewhaleMissions(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    status = models.IntegerField()
    golive = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_missions'


class LivewhaleModules(models.Model):
    name = models.CharField(unique=True, max_length=255)
    revision = models.FloatField()

    class Meta:
        managed = False
        db_table = 'livewhale_modules'


class LivewhaleNews(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True, null=True, default=None)
    parent = models.IntegerField(blank=True, null=True)
    headline = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date = models.CharField(max_length=255)
    date_dt = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=1000, blank=True, null=True)
    rank = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(blank=True, null=True, default=settings.BRIDGE_USER)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True, default=None)
    is_starred = models.IntegerField(blank=True, null=True)
    golive = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    gallery_id = models.IntegerField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True, default=None)
    has_invalid_url = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_news'

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        return "https://www.carthage.edu/live/news/{}/".format(self.id)

    def tag(self, jid=None):
        return get_tag(self.id,jid)

    def image(self):
        foto = None
        img =  LivewhaleImages2Any.objects.using('livewhale').filter(id2=self.id).filter(type="news")
        if img:
            foto = LivewhaleImages.objects.using('livewhale').get(pk=img[0].id1)
        return foto

    def new(self):
        return LivewhaleTags2Any.objects.using('livewhale').filter(
            id2=self.id
        ).filter(type="news").filter(
            id1=settings.BRIDGE_NEW_TAG
        )

    def save(self, data=None, *args, **kwargs):
        self.headline = strip_tags(self.headline).encode('utf8')
        self.summary = strip_tags(self.summary).encode('utf8')
        self.body = self.body.encode('utf8')

        # dates
        NOW  = datetime.datetime.now()
        TODAY = datetime.date.today()
        # set contact info from request.user
        if data:
            u = data["user"]
            self.contact_info = '<p><a href="mailto:{}">{} {}</a></p>'.format(
                u.email, u.first_name, u.last_name
            )
            if in_group(u, "carthageStaffStatus", "carthageFacultyStatus"):
                self.status = 1
            else: # student
                self.status = 0
        # save
        super(LivewhaleNews, self).save(*args, **kwargs)

        """
        We have to resort to MySQLdb because:
            a) livewhale uses UTC for events but not for news
            b) Django does not support composite Foreign Keys
        """
        if data:
            #cursor = connection.cursor()

            # tag the category
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    ({}, {}, 'news')
            """.format(data["category"], self.id)
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale",ssl=SSL)
            # tag it "New"
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    ({}, {}, 'news')
            """.format(settings.BRIDGE_NEW_TAG, self.id)
            mysql_db(sql,db="livewhale",ssl=SSL)

            # set dates outside of django timezone aware ecosystem
            # since livewhale does not use UTC for news items
            if not self.views:
                date = NOW.strftime("%m/%d/%Y")
                date_dt = datetime.datetime.combine(
                    TODAY, datetime.time()
                )
                sql = """
                    UPDATE
                        livewhale_news
                    SET
                        views = 1,
                        date = "{}",
                        date_dt = "{}",
                        date_created = "{}",
                        last_modified = "{}"
                    WHERE
                        id = {}
                """.format(date, date_dt, NOW, NOW, self.id)
            else:
                sql = """
                    UPDATE
                        livewhale_news
                    SET
                        last_modified = "{}"
                    WHERE
                        id = {}
                """.format(NOW, self.id)
            mysql_db(sql,db="livewhale",ssl=SSL)


class LivewhaleNews2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_news2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhalePages(models.Model):
    id = models.AutoField(unique=True)
    gid = models.IntegerField(blank=True, null=True)
    gids = models.CharField(max_length=1000, blank=True, null=True)
    uids = models.CharField(max_length=1000, blank=True, null=True)
    path = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    depth = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField(blank=True, null=True)
    content = models.TextField()
    elements = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    is_editing_ts = models.IntegerField(blank=True, null=True)
    is_editing_user = models.IntegerField(blank=True, null=True)
    is_template = models.IntegerField(blank=True, null=True)
    host = models.CharField(primary_key=True, max_length=50)
    ga_year = models.IntegerField(blank=True, null=True)
    ga_month = models.IntegerField(blank=True, null=True)
    ga_week = models.IntegerField(blank=True, null=True)
    ga_keywords = models.CharField(max_length=500, blank=True, null=True)
    schedule = models.CharField(max_length=1000, blank=True, null=True)
    schedule_expires = models.DateTimeField(blank=True, null=True)
    schedule_expires_type = models.IntegerField(blank=True, null=True)
    schedule_to_type = models.IntegerField(blank=True, null=True)
    schedule_to_email = models.CharField(max_length=255, blank=True, null=True)
    diff = models.TextField(blank=True, null=True)
    subscriptions = models.TextField(blank=True, null=True)
    subscriptions_date = models.DateTimeField(blank=True, null=True)
    total_errors = models.IntegerField(blank=True, null=True)
    is_draft = models.IntegerField(blank=True, null=True)
    is_draft_closure = models.IntegerField(blank=True, null=True)
    accessibility_score = models.CharField(max_length=50, blank=True, null=True)
    accessibility_report = models.TextField(blank=True, null=True)
    tid = models.IntegerField(blank=True, null=True)
    thash = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    has_editable_regions = models.IntegerField(blank=True, null=True)
    is_details_template = models.IntegerField(blank=True, null=True)
    is_no_editing = models.IntegerField(blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    is_section = models.IntegerField(blank=True, null=True)
    admin_only_elements = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_pages'
        unique_together = (('host', 'id'),)

    def __unicode__(self):
        return self.short_title.decode('utf-8')

    def get_absolute_url(self):
        return 'https://www.carthage.edu{}/'.format(self.directory)


class LivewhalePages2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_pages2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhalePagesAuthorization(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=255)
    host = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_authorization'


class LivewhalePagesNavs(models.Model):
    gid = models.IntegerField()
    title = models.CharField(max_length=255)
    host = models.CharField(max_length=50)
    is_main = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_navs'


class LivewhalePagesNavsItems(models.Model):
    pid = models.IntegerField()
    depth = models.IntegerField(blank=True, null=True)
    host = models.CharField(max_length=50, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=4)
    status = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_navs_items'


class LivewhalePagesNotes(models.Model):
    pid = models.IntegerField()
    uid = models.IntegerField()
    date = models.DateTimeField()
    type = models.IntegerField()
    note = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_notes'


class LivewhalePagesRevisions(models.Model):
    id = models.AutoField(unique=True)
    gid = models.IntegerField(blank=True, null=True)
    gids = models.CharField(max_length=1000, blank=True, null=True)
    uids = models.CharField(max_length=1000, blank=True, null=True)
    pid = models.IntegerField()
    path = models.CharField(max_length=255)
    directory = models.CharField(max_length=255)
    depth = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    short_title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField(blank=True, null=True)
    content = models.TextField()
    elements = models.TextField()
    note = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(primary_key=True, max_length=50)
    ga_year = models.IntegerField(blank=True, null=True)
    ga_month = models.IntegerField(blank=True, null=True)
    ga_week = models.IntegerField(blank=True, null=True)
    ga_keywords = models.CharField(max_length=500, blank=True, null=True)
    schedule = models.CharField(max_length=1000, blank=True, null=True)
    schedule_expires = models.DateTimeField(blank=True, null=True)
    schedule_expires_type = models.IntegerField(blank=True, null=True)
    schedule_to_type = models.IntegerField(blank=True, null=True)
    schedule_to_email = models.CharField(max_length=255, blank=True, null=True)
    diff = models.TextField(blank=True, null=True)
    subscriptions = models.TextField(blank=True, null=True)
    subscriptions_date = models.DateTimeField(blank=True, null=True)
    total_errors = models.IntegerField(blank=True, null=True)
    is_draft = models.IntegerField(blank=True, null=True)
    is_draft_closure = models.IntegerField(blank=True, null=True)
    accessibility_score = models.CharField(max_length=50, blank=True, null=True)
    accessibility_report = models.TextField(blank=True, null=True)
    tid = models.IntegerField(blank=True, null=True)
    thash = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    has_editable_regions = models.IntegerField(blank=True, null=True)
    is_details_template = models.IntegerField(blank=True, null=True)
    is_no_editing = models.IntegerField(blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    is_section = models.IntegerField(blank=True, null=True)
    admin_only_elements = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_revisions'
        unique_together = (('host', 'id'),)


class LivewhalePagesTemplates(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    path = models.CharField(max_length=255)
    host = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'livewhale_pages_templates'


class LivewhalePaymentsOrders(models.Model):
    gid = models.IntegerField()
    gateway = models.CharField(max_length=50)
    gateway_response = models.CharField(max_length=10000, blank=True, null=True)
    order_quantity = models.IntegerField()
    order_total = models.CharField(max_length=11)
    order_date = models.DateTimeField()
    product_description = models.CharField(max_length=255)
    product_type = models.CharField(max_length=50, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=50, blank=True, null=True)
    customer_address = models.CharField(max_length=50, blank=True, null=True)
    customer_city = models.CharField(max_length=50, blank=True, null=True)
    customer_state = models.CharField(max_length=50, blank=True, null=True)
    customer_zip = models.CharField(max_length=50, blank=True, null=True)
    customer_country = models.CharField(max_length=50, blank=True, null=True)
    custom_fields = models.CharField(max_length=10000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_payments_orders'


class LivewhalePaymentsSettings(models.Model):
    gid = models.IntegerField(primary_key=True)
    gateway = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_payments_settings'
        unique_together = (('gid', 'name'),)


class LivewhalePlaces(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    keywords = models.CharField(max_length=500, blank=True, null=True)
    is_preset = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    thumb = models.CharField(max_length=255, blank=True, null=True)
    requires_reservation = models.IntegerField(blank=True, null=True)
    reservation_instructions = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_places'


class LivewhalePlaces2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_places2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleProfiles(models.Model):
    gid = models.IntegerField()
    tid = models.IntegerField(blank=True, null=True)
    suggested = models.CharField(max_length=500, blank=True, null=True)
    parent = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True, default=1)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_starred = models.IntegerField(blank=True, null=True)
    gallery_id = models.IntegerField(blank=True, null=True)
    is_shared = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField()
    contact_info = models.CharField(max_length=1000, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    sync_keys = models.TextField(blank=True, null=True)
    has_invalid_url = models.IntegerField(blank=True, null=True)
    golive = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField(blank=True, null=True)
    is_archived = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_profiles'


class LivewhaleProfiles2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_profiles2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleProfilesDataSources(models.Model):
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    configuration = models.TextField()
    all_fields = models.TextField()
    key_field = models.CharField(max_length=255)
    refresh_rate = models.IntegerField()
    last_refresh = models.DateTimeField()
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_profiles_data_sources'


class LivewhaleProfilesFields(models.Model):
    pid = models.IntegerField()
    fid = models.IntegerField()
    value = models.TextField(blank=True, null=True)
    is_private = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_profiles_fields'


class LivewhaleProfilesTypes(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)
    is_restricted = models.IntegerField(blank=True, null=True)
    style = models.IntegerField()
    is_private = models.IntegerField(blank=True, null=True)
    auto_authorize = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_profiles_types'


class LivewhaleProfilesTypesFields(models.Model):
    pid = models.IntegerField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    position = models.IntegerField()
    allow_in_linked = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    sync_id = models.IntegerField(blank=True, null=True)
    sync_name = models.CharField(max_length=255, blank=True, null=True)
    instructional_text = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.IntegerField(blank=True, null=True)
    field_options = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_profiles_types_fields'


class LivewhaleProfilesTypesStandardFields(models.Model):
    pid = models.IntegerField()
    title = models.CharField(max_length=255)
    sync_id = models.IntegerField(blank=True, null=True)
    sync_name = models.CharField(max_length=255, blank=True, null=True)
    instructional_text = models.CharField(max_length=255, blank=True, null=True)
    is_enabled = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_required = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_profiles_types_standard_fields'


class LivewhalePublicSubmissions(models.Model):
    submitter_id = models.IntegerField()
    submission_id = models.IntegerField()
    submission_type = models.CharField(max_length=255)
    submission_title = models.CharField(max_length=255)
    submission_date = models.DateTimeField()
    mission_id = models.IntegerField(blank=True, null=True)
    mission_title = models.CharField(max_length=500, blank=True, null=True)
    has_copies = models.IntegerField(blank=True, null=True)
    from_livewhale_reporter = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_public_submissions'


class LivewhalePublicSubmitters(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_public_submitters'


class LivewhaleRedirects(models.Model):
    host = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    last_used = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_redirects'


class LivewhaleRevisions(models.Model):
    pid = models.IntegerField()
    uid = models.IntegerField()
    type = models.CharField(max_length=255)
    date = models.DateTimeField()
    revision = models.TextField(blank=True, null=True)
    search = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_revisions'


class LivewhaleScheduler(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    exec_field = models.CharField(db_column='exec', max_length=255)  # Field renamed because it was a Python reserved word.
    next_execution = models.DateTimeField()
    frequency = models.IntegerField()
    env = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'livewhale_scheduler'


class LivewhaleSearch(models.Model):
    type = models.CharField(primary_key=True, max_length=255)
    pid = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    high_content = models.CharField(max_length=1000, blank=True, null=True)
    medium_content = models.CharField(max_length=5000, blank=True, null=True)
    low_content = models.TextField(blank=True, null=True)
    phrases = models.CharField(max_length=5000, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_search'
        unique_together = (('type', 'pid'),)


class LivewhaleSearchData(models.Model):
    phrase = models.CharField(primary_key=True, max_length=50)
    type = models.CharField(max_length=10)
    target_title = models.CharField(max_length=50)
    target_url = models.CharField(max_length=100)
    date_searched = models.DateField()
    total = models.IntegerField()
    last_modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'livewhale_search_data'
        unique_together = (('phrase', 'type', 'target_url', 'date_searched'),)


class LivewhaleTags(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    is_starred = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_tags'


class LivewhaleTags2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_tags2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleUrls(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_urls'


class LivewhaleUrls2Any(models.Model):
    id1 = models.IntegerField(primary_key=True)
    id2 = models.IntegerField()
    type = models.CharField(max_length=255)
    position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'livewhale_urls2any'
        unique_together = (('id1', 'id2', 'type'),)


class LivewhaleUrlsShortened(models.Model):
    url = models.CharField(max_length=1000)
    date_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_urls_shortened'


class LivewhaleUsers(models.Model):
    gid = models.IntegerField()
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    last_access = models.DateTimeField(blank=True, null=True)
    authorized_modules = models.CharField(max_length=500, blank=True, null=True)
    use_email = models.CharField(max_length=1, blank=True, null=True)
    switch_groups = models.CharField(max_length=5000, blank=True, null=True)
    total_errors = models.IntegerField(blank=True, null=True)
    tag = models.IntegerField(blank=True, null=True)
    navigation = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_users'


class LivewhaleUsersSettings(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_users_settings'
        unique_together = (('uid', 'name'),)


class LivewhaleUsersShortcuts(models.Model):
    uid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'livewhale_users_shortcuts'
        unique_together = (('uid', 'url'),)


class LivewhaleWidgetCache(models.Model):
    request_key = models.CharField(primary_key=True, max_length=32)
    widget_key = models.CharField(max_length=32)
    partition_key = models.IntegerField()
    host = models.CharField(max_length=50)
    ip = models.CharField(max_length=45)
    page = models.CharField(max_length=255)
    query = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20)
    gids = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    last_modified = models.DateTimeField()
    expires = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    content_vars = models.TextField(blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    parent = models.CharField(max_length=1625, blank=True, null=True)
    visibility = models.CharField(max_length=7)
    language = models.CharField(max_length=20)
    gid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_widget_cache'
        unique_together = (('request_key', 'widget_key', 'partition_key'),)


class LivewhaleWidgets(models.Model):
    gid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    args = models.CharField(max_length=10000)
    date_created = models.DateTimeField()
    last_modified = models.DateTimeField()
    last_user = models.IntegerField()
    syntax = models.CharField(max_length=10000, blank=True, null=True)
    auto_authorize = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'livewhale_widgets'

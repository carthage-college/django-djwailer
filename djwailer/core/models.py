# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models, connection
from django.utils.html import strip_tags
from django.template.defaultfilters import removetags

from djtools.utils.database import mysql_db
from djtools.utils.users import in_group

import datetime

CATEGORIES = (
    ('','---------'),
    ('498','News & Notices'),
    ('499','Lectures & Presentations'),
    ('500','Arts & Performances'),
    ('477','Kudos'),
    ('501','Faculty & Staff News'),
    ('502','Student News'),
    ('504','Library & Technology'),
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'livewhale_course_catalog'

class LivewhaleEvents(models.Model):
    gid = models.IntegerField(default=settings.BRIDGE_GROUP)
    suggested = models.CharField(max_length=500, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    eid = models.CharField(max_length=255, blank=True, default="")
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
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    source = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(default=1)
    location = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_user = models.IntegerField(default=settings.BRIDGE_USER)
    created_by = models.IntegerField(
        null=True, blank=True, default=settings.BRIDGE_USER
    )
    # lw1.6
    #lookup = models.CharField(max_length=255, blank=True)
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
    registration_notifications_email = models.CharField(
        max_length=255, blank=True
    )
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
    subscription_id = models.CharField(max_length=255, blank=True, default=None)
    subscription_pid = models.IntegerField(null=True, blank=True)
    # lw15
    is_canceled = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = u'livewhale_events'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "https://www.carthage.edu/live/events/{}/".format(self.id)

    def save(self, data=None, *args, **kwargs):
        self.title = removetags(self.title, 'style').encode('utf8')
        self.summary = removetags(self.summary, 'style').encode('utf8')
        self.description = self.description.encode('utf8')
        self.location = removetags(self.location, 'style').encode('utf8')

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
            mysql_db(sql,db="livewhale")
            # category
            sql = """
                INSERT INTO livewhale_events_categories2any
                    (id1, id2, type)
                VALUES
                    ({}, {}, 'events')
            """.format(30,self.id)
            #cursor.execute(sql)
            mysql_db(sql,db="livewhale")

class LivewhaleEvents2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()

    class Meta:
        db_table = u'livewhale_events2any'

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
    # lw1.6
    #lookup = models.CharField(max_length=765, blank=True)
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
    headline = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    status = models.IntegerField(default=1)
    date = models.CharField(max_length=255,default="")
    date_dt = models.DateTimeField(auto_now_add=True)
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
    # lw1.6
    #lookup = models.CharField(max_length=255, blank=True, default=None)
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
        self.headline = removetags(self.headline, 'style').encode('utf8')
        self.summary = removetags(self.summary, 'style').encode('utf8')
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
            mysql_db(sql,db="livewhale")
            # tag it "New"
            sql = """
                INSERT INTO livewhale_tags2any
                    (id1, id2, type)
                VALUES
                    ({}, {}, 'news')
            """.format(settings.BRIDGE_NEW_TAG, self.id)
            mysql_db(sql,db="livewhale")

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
            mysql_db(sql,db="livewhale")


class LivewhaleNews2Any(models.Model):
    id1 = models.IntegerField()
    id2 = models.IntegerField()
    type = models.CharField(max_length=765, primary_key=True)
    position = models.IntegerField()

    class Meta:
        db_table = u'livewhale_news2any'

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
    # lw1.6
    #lookup = models.CharField(max_length=765, blank=True)
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

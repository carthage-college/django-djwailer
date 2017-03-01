#-- coding: utf-8 --
import datetime
from haystack import indexes
from djwailer.core.models import LivewhalePages


class LivewhalePageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True, use_template=True
    )
    short_title = indexes.CharField(model_attr='short_title')
    date_created = indexes.DateTimeField(model_attr='date_created')
    last_modified = indexes.DateTimeField(model_attr='last_modified')

    def get_model(self):
        return LivewhalePages

    def get_url(self, obj):
        return obj.get_absolute_url()

    #def get_title(self, obj):
    #    return obj.short_title.decode('utf-8')

    def prepare_short_title(self, obj):
        return obj.short_title.decode('utf-8')

    def index_queryset(self, using=None):
        '''
        Used when the entire index for model is updated.
        '''
        return self.get_model().objects.filter(
            date_created__lte=datetime.datetime.now()
        )

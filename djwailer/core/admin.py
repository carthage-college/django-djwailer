# -*- coding: utf-8 -*-

from django.contrib import admin
from djwailer.core.models import LivewhaleCourseCatalog


class LivewhaleCourseCatalogAdmin(admin.ModelAdmin):
    """Data model class for the course catalog in livewhale."""

    list_display = ('title', 'crs_no', 'cat', 'dept', 'credits', 'sess', 'terms')
    search_fields = ('title', 'crs_no', 'cat', 'dept', 'credits', 'sess', 'terms')
    using = "livewhale"

    def save_model(self, request, instance, form, change):
        """Tell Django to save objects to the 'other' database."""
        instance.save(using=self.using)

    def delete_model(self, request, instance):
        """Tell Django to delete objects from the 'other' database."""
        instance.delete(using=self.using)

    def get_queryset(self, request):
        """Tell Django to look for objects on the 'other' database."""
        return super(
            LivewhaleCourseCatalogAdmin, self,
        ).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """Populate ForeignKey widgets using a query on 'other' database."""
        return super(
            LivewhaleCourseCatalogAdmin, self,
        ).formfield_for_foreignkey(
            db_field, request=request, using=self.using, **kwargs,
        )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        """Populate ManyToMany widgets using a query on 'other' database."""
        return super(
            LivewhaleCourseCatalogAdmin, self,
        ).formfield_for_manytomany(
            db_field, request=request, using=self.using, **kwargs,
        )


admin.site.register(LivewhaleCourseCatalog, LivewhaleCourseCatalogAdmin)

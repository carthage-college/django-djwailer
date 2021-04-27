# -*- coding: utf-8 -*-

"""URLs for all views."""

from django.urls import path
from django.views.generic import RedirectView
from djwailer.bridge import views


urlpatterns = [
    path('unicode/<int: oid>)/', views.unicode_test, name='unicode_test'),
    path(
        '<str:content_type>/success/',
        views.submission_success,
        name='submission_success',
    ),
    path('<str:content_type>/', views.submission_form, name='submission_form'),
    path('', RedirectView.as_view(url="/bridge/")),
]

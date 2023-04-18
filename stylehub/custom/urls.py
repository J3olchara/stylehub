"""Endpoints of custom app"""
import django.urls

import custom.views

app_name = 'custom'

urlpatterns = [
    django.urls.path(
        '',
        custom.views.Main.as_view(),
        name='main',
    ),
]

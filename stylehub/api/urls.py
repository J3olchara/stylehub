"""APP api URL Configuration"""
from typing import List

from api import views
from django.urls import path, resolvers

app_name = 'api'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'toggle_liked/<int:item_id>',
        views.ToggleLiked.as_view(),
        name='toggle_liked',
    ),
]

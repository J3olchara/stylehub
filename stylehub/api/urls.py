"""APP api URL Configuration"""
from typing import List

from django.urls import path, resolvers

from api import views

app_name = 'api'

urlpatterns: List[resolvers.URLPattern] = [
    path('toggle_liked/<int:item_id>', views.ToggleLiked.as_view(), name='toggle_liked'),
]

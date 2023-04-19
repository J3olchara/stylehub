"""APP api URL Configuration"""
from typing import List

from django.urls import path, resolvers


from api import views

app_name = 'api'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'delete_order_custom/<int:pk>',
        views.ToggleLiked.as_view(),
        name='delete_order_custom',
    ),
]

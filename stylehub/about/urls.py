"""APP about URL Configuration"""
from typing import List

from about import views
from django.urls import path, resolvers

app_name = 'about'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.AboutUsView.as_view(), name='about'),
]

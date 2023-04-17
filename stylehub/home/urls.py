"""APP home URL Configuration"""
from typing import List

from django.urls import path, resolvers

from home import views

app_name = 'home'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.Home.as_view(), name='home'),
]

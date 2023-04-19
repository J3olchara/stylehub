"""Endpoints of custom app"""
import django.urls

import custom.views

app_name = 'custom'

urlpatterns = [
    django.urls.path(
        '',
        custom.views.Main.as_view(),
        name='home',
    ),
    django.urls.path(
        'order_detail/<int:pk>',
        custom.views.CustomDetail.as_view(),
        name='order_detail',
    ),
]

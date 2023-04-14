"""stylehub URL Configuration"""
from django.contrib import admin
from django.urls import include, path

import market.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('market/', include(market.urls)),
]

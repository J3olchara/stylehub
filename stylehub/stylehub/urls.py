"""stylehub URL Configuration"""
import django.urls
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    django.urls.path('admin/', admin.site.urls),
    django.urls.path('clothes/', django.urls.include('clothes.urls')),
]


if settings.DEBUG:
    import debug_toolbar.urls

    urlpatterns += [
        django.urls.path('__debug__/', django.urls.include(debug_toolbar.urls))
    ]

"""stylehub URL Configuration"""
from typing import Any

import django.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns: Any = [
    django.urls.path('admin/', admin.site.urls),
    django.urls.path('', django.urls.include('home.urls')),
    django.urls.path('auth/', django.urls.include('auth.urls')),
    django.urls.path('clothes/', django.urls.include('clothes.urls')),
    django.urls.path('custom/', django.urls.include('custom.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar.urls

    urlpatterns += [
        django.urls.path('__debug__/', django.urls.include(debug_toolbar.urls))
    ]

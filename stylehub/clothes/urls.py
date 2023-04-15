"""
clothes shop urlpatterns

add here your views
"""
import django.urls

import clothes.views

app_name = 'clothes'

urlpatterns = [
    django.urls.path(
        'wear/<int:pk>/', clothes.views.Wear.as_view(), name='wear'
    ),
    django.urls.path(
        'collection/<int:pk>/',
        clothes.views.Collection.as_view(),
        name='collection_detail',
    ),
]

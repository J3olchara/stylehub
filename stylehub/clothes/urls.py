"""
clothes shop urlpatterns

add here your views
"""
import django.urls

import clothes.views

app_name = 'clothes'

urlpatterns = [
    django.urls.path(
        '',
        clothes.views.Main.as_view(),
        name='main',
    ),
    django.urls.path(
        'collections/',
        clothes.views.PopularCollections.as_view(),
        name='collections',
    ),
    django.urls.path(
        'designers/',
        clothes.views.PopularDesigners.as_view(),
        name='designers',
    ),
    django.urls.path(
        'unpopular/',
        clothes.views.UnpopularItems.as_view(),
        name='unpopular',
    ),
    django.urls.path(
        'wear/<int:pk>/', clothes.views.Wear.as_view(), name='wear'
    ),
    django.urls.path(
        'collection/<int:pk>/',
        clothes.views.Collection.as_view(),
        name='collection',
    ),
    django.urls.path(
        'designer/<int:pk>/',
        clothes.views.Designer.as_view(),
        name='designer',
    ),
    django.urls.path(
        'recommend/',
        clothes.views.Recommend.as_view(),
        name='recommend',
    ),
]

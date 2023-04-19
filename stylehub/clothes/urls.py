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
    django.urls.path(
        'create/<str:form>/',
        clothes.views.CreateSomething.as_view(),
        name='create',
    ),
    django.urls.path('orders/', clothes.views.Orders.as_view(), name='orders'),
    django.urls.path(
        'lovely/', clothes.views.Lovely.as_view(), name='lovely_designers'
    ),
    django.urls.path('orders/', clothes.views.Orders.as_view(), name='orders'),
    django.urls.path(
        'lovely/', clothes.views.Lovely.as_view(), name='lovely_designers'
    ),
    django.urls.path(
        'liked/', clothes.views.Saved.as_view(), name='liked_items'
    ),
]

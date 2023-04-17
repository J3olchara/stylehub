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
<<<<<<< Updated upstream
        name='collection_detail',
=======
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
>>>>>>> Stashed changes
    ),
]

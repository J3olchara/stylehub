"""APP api URL Configuration"""
from typing import List

from api import views
from django.urls import path, resolvers

app_name = 'api'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'delete_order_custom/<int:pk>',
        views.DeleteOrderCustom.as_view(),
        name='delete_order_custom',
    ),
    path(
        'update_order_status/<int:pk>',
        views.UpdateOrderCustomStatus.as_view(),
        name='update_order_custom_status',
    ),
    path(
        'take_a_order_custom/<int:pk>',
        views.GiveOrderCustomToDesigner.as_view(),
        name='get_order_custom_to_designers',
    ),
]

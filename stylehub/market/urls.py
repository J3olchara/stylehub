""" market app urls configuration """
from typing import List

from django.urls import path, resolvers

import market.views

app_name: str = 'market'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'collection/<int:collection_number>',
        market.views.CollectionDetails.as_view(),
        name='collection_detail',
    )
]

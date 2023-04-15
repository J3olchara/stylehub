"""
page views for clothes shop

write your clothes shop views here
"""
from typing import TYPE_CHECKING

from django.views import generic

import market.models

if TYPE_CHECKING:
    WearDetailView = generic.DetailView[market.models.Item]
    CollectionDetailView = generic.DetailView[market.models.Collection]
else:
    WearDetailView = generic.DetailView
    CollectionDetailView = generic.DetailView


class Wear(WearDetailView):
    """gives an item information"""

    model = market.models.Item
    template_name = 'clothes/wear.html'
    context_object_name = 'item'


class Collection(CollectionDetailView):
    """gives an collection information"""

    model = market.models.Collection
    template_name = 'clothes/collection.html'
    context_object_name = 'collection'

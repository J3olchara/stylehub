"""
page views for clothes shop

write your clothes shop views here
"""
from typing import Any

from django.db.models import QuerySet
from django.views import generic

import market.models


class Wear(generic.DetailView[market.models.Item]):
    """gives an item information"""

    template_name = 'clothes/wear.html'
    context_object_name = 'item'
    queryset = market.models.Item.objects.get_details()


class Collection(generic.DetailView[market.models.Collection]):
    """gives a collection information"""

    template_name = 'clothes/collection.html'
    queryset = market.models.Collection.objects.get_items_in_collection()
    context_object_name = 'collection'


class Recommend(generic.ListView[market.models.Collection]):
    """gives a popular collections based on user seen history"""

    template_name = 'clothes/recommend.html'
    context_object_name = 'collections'

    def get_queryset(self) -> QuerySet[Any]:
        """get popular collections queryset"""
        return market.models.Collection.objects.recommend(self.request.user)

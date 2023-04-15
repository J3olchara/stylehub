"""
page views for clothes shop

write your clothes shop views here
"""
from django.views import generic

import market.models


class Wear(generic.DetailView[market.models.Item]):
    """gives an item information"""

    model = market.models.Item
    template_name = 'clothes/wear.html'
    context_object_name = 'item'


class Collection(generic.DetailView[market.models.Collection]):
    """gives an collection information"""

    template_name = 'clothes/collection.html'
    queryset = market.models.Collection.objects.get_items_in_collection()
    context_object_name = 'collection'

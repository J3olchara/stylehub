"""
page views for clothes shop

write your clothes shop views here
"""
from django.views import generic

import market.models


class Wear(generic.DetailView[market.models.Item]):
    """gives an item information"""

    template_name = 'clothes/wear.html'
    context_object_name = 'item'
    queryset = market.models.Item.objects.get_details()

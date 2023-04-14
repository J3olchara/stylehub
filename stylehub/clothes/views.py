"""
page views for clothes shop

write your clothes shop views here
"""
from typing import TYPE_CHECKING

from django.views import generic

import market.models

if TYPE_CHECKING:
    WearDetailView = generic.DetailView[market.models.Item]
else:
    WearDetailView = generic.DetailView


class Wear(WearDetailView):
    """gives an item information"""

    model = market.models.Item
    template_name = 'clothes/wear.html'
    context_object_name = 'item'

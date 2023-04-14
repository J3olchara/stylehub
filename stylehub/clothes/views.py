"""
page views for clothes shop

write your clothes shop views here
"""
from django.views import generic

import market.models


class Wear(generic.DetailView):
    model = market.models.Item
    template_name = 'clothes/wear.html'
    context_object_name = 'item'
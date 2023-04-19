"""HOMEPAGE app pages views"""
import django.views.generic
from django.db.models.query import QuerySet

import clothes.models


class Home(django.views.generic.ListView['clothes.models.Item']):
    """returns homepage"""

    template_name = 'home/index.html'
    context_object_name = 'items'

    def get_queryset(self) -> QuerySet['clothes.models.Item']:
        """returns items"""
        return clothes.models.Item.objects.all()#.get_like_status(self.request.user)

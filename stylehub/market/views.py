""" Funcions which are using in all project"""
from typing import Any, Dict

from django.views.generic import TemplateView

import market.models


class CollectionDetails(TemplateView):
    """View for see all items in collection"""

    template_name: str = 'market/collection_detail.html'
    model = market.models.Item

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        collection_number: int = self.kwargs.get('collection_number')
        context['items'] = market.models.Item.objects.get_collections_items(
            collection_number
        )
        return context

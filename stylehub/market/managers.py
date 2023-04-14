""" Managers for models in market.models """
from typing import TYPE_CHECKING, Any

from django.apps import apps
from django.db import models

if TYPE_CHECKING:
    BaseManager = models.Manager[Any]
else:
    BaseManager = models.Manager


class ItemManager(BaseManager):
    """Manager for Item model"""

    def get_collections_items(
        self, collection_number: int
    ) -> models.query.QuerySet[Any]:
        """Returns Item, which belongs collection with
        id=collection_number"""
        self.model: Any = apps.get_model('market', 'Item')
        style: Any = apps.get_model('market', 'Style')
        prefetch_styles: Any = models.Prefetch(
            self.model.styles.field.name,
            queryset=style.objects.only(
                style.name.field.name,
            ),
        )
        return (
            self.get_queryset()
            .filter(collection__id=collection_number)
            .select_related('collection')
            .select_related('category')
            .prefetch_related(prefetch_styles)
        )

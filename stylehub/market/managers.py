""" Managers for models in market.models """
from typing import Any

from django.apps import apps
from django.db import models


class CollectionManager(models.Manager[Any]):
    """Manager for Collection model"""

    def get_items_in_collection(self) -> models.query.QuerySet[Any]:
        """Returns Item, which belongs collection"""
        item: Any = apps.get_model('market', 'Item')
        style: Any = apps.get_model('market', 'Style')
        image: Any = apps.get_model('market', 'ItemPicture')
        prefetch_images = models.Prefetch(
            'images',
            queryset=image.objects.all().only(image.picture.field.name),
        )
        item_queryset = (
            item.objects.filter(is_published=True)
            .select_related(item.category.field.name)
            .prefetch_related(prefetch_images)
        )

        prefetch_items = models.Prefetch('items', queryset=item_queryset)

        prefetch_styles = models.Prefetch(
            self.model.style.field.name,
            queryset=style.objects.only(style.name.field.name),
        )

        return (
            self.get_queryset()
            .prefetch_related(prefetch_items)
            .prefetch_related(prefetch_styles)
        )

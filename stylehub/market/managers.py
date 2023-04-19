"""managers for market app"""
from typing import Any

from django.apps import apps
from django.db import models


class StyleManager(models.Manager[Any]):
    """manager for style nodel"""

    def all(self) -> models.QuerySet[Any]:
        """custom all method"""
        style: Any = apps.get_model('market', 'Style')
        return super().all().order_by(style.name.field.name)


class CategoryExtendedManager(models.Manager[Any]):
    """manager for style nodel"""

    def all(self) -> models.QuerySet[Any]:
        """custom all method"""
        category_extended: Any = apps.get_model('market', 'CategoryExtended')
        return super().all().order_by(category_extended.name.field.name)

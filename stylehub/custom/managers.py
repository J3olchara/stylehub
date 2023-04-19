"""Manaers for custom app models"""
from typing import Any

from django.db import models


class OrdersManager(models.Manager[Any]):
    """Manager for OrderCustom model"""

    def get_free_orders(self) -> models.QuerySet[Any]:
        """Returns CustomOrders withoit designers"""
        return (
            self.get_queryset()
            .filter(designer__isnull=True)
            .order_by(f'-{self.model.created.field.name}')
        )

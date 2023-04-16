"""Managers for clothes models"""
from typing import Any, Union

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import Case, Value, When

import auth.models


class OrderClothesManager(models.Manager[Any]):
    """Manager for OrderClothes model in clothes app"""

    def get_user_orders(
        self, user: Union['auth.models.User', AnonymousUser]
    ) -> models.QuerySet[Any]:
        """get users orders"""
        return (
            self.get_queryset()
            .filter(user=user)
            .select_related(self.model.item.field.name)
            .order_by(
                Case(When(status='done', then=Value(1)), default=Value(0)),
                f'-{self.model.edited.field.name}',
            )
        )

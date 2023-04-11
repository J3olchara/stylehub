"""models for auth"""
from typing import Any, Union

import market.models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended User model from AbstractUser

    last_category: market.models.Category. Last seen user category.
    last_styles: market.models.category[:5]. Five last seen styles.
    """

    last_category: Union[
        models.query.QuerySet[market.models.CategoryExtended],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        verbose_name='Последняя посещённая категория',
        to=market.models.CategoryExtended,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    last_styles: Union[
        models.query.QuerySet[market.models.Style],
        'models.ManyToManyField[Any, Any]',
    ] = models.ManyToManyField(
        verbose_name='Последние пять посещённых стилей', to=market.models.Style
    )

    def clean(self) -> None:
        if self.last_styles.count() > 5:
            self.last_styles = self.last_styles[-5:]
        return super().clean()

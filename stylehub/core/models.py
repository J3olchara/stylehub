"""CORE abstract models"""
from datetime import datetime
from typing import Any, Union

from django.db import models

import core.utils


class BaseCreature(models.Model):
    """
    BaseCreature model for models like category, tag< style and other

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    """

    name: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
        verbose_name='название',
        help_text='Придумайте название',
        max_length=50,
        blank=False,
        null=False,
    )
    slug: Union[str, 'models.SlugField[Any, Any]'] = models.SlugField(
        verbose_name='слаг',
        help_text='Нормализованное имя',
        unique=True,
    )
    created: Union[
        datetime, 'models.DateTimeField[Any, Any]'
    ] = models.DateTimeField(
        verbose_name='дата и время создания',
        help_text='Автоматически выставляется при создании',
        auto_now_add=True,
        blank=False,
        null=False,
    )
    edited: Union[
        datetime,
        'models.DateTimeField[Any, Any]',
    ] = models.DateTimeField(
        verbose_name='дата и время последнего редактирования',
        help_text='Автоматически выставляется при изменении объекта',
        auto_now=True,
        blank=False,
        null=False,
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.slug = self.get_slug()
        return super().save(*args, **kwargs)

    def get_slug(self) -> str:
        """

        :return: normalized name
        """
        slug: str = self.name.upper()
        translate_tab = str.maketrans(core.utils.normalize_table)
        return slug.translate(translate_tab)

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'

    class Meta:
        """Model settings"""

        abstract = True

"""CORE abstract models"""
from datetime import datetime
from typing import Any, Union

from django.core.exceptions import ValidationError
from django.db import models

import core.utils


class CreatedEdited(models.Model):
    """
    Model for models that uses creation date and editing date

    created: datetime. creation datetime
    edited: datetime. editing datetime
    """

    created: Union[datetime, Any] = models.DateTimeField(
        verbose_name='дата и время создания',
        help_text='Когда объект был создан',
        auto_now_add=True,
    )
    edited: Union[datetime, Any] = models.DateTimeField(
        verbose_name='дата и время редактирования',
        help_text='Когда объект в последний раз редактировали',
        auto_now=True,
    )

    class Meta:
        """settings for creatededited model"""

        abstract = True


class BaseCreature(CreatedEdited):
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

    def clean(self) -> None:
        self.slug = self.get_slug()
        if type(self).objects.filter(slug=self.slug).exists():
            raise ValidationError('Объект с таким именем уже существует')
        self.name = self.name.capitalize()
        return super().clean()

    def get_slug(self) -> str:
        """
        creates slug by translating object username
        :return: normalized name
        """
        slug: str = self.name.upper()
        translate_tab = str.maketrans(core.utils.normalize_table)
        return slug.translate(translate_tab).lower()

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'

    class Meta:
        """Model settings"""

        abstract = True

"""Market models"""
from datetime import datetime
from typing import Any, Union

from django.db import models

import auth.models
import core.models


class Style(core.models.BaseCreature):
    """
    style model for items filter
    describes item style: alternative, elitary and other.

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    text: string. style describing.
    """

    text = models.TextField(
        verbose_name='описание стиля',
        help_text='Опишите стиль, добавьте интересные факты',
        blank=True,
        null=True,
    )

    class Meta:
        """Model settings"""

        ordering = (
            core.models.BaseCreature.created.field.name,
            core.models.BaseCreature.name.field.name,
        )


class CategoryExtended(core.models.BaseCreature):
    """
    category model for items filter
    describes item category: hoodie, pants and other.

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    """

    category_base = models.ForeignKey(
        verbose_name='базовая категория вещи',
        help_text=(
            'Объясните способ носки вещи: '
            'верхняя одежда, нижнее бельё, шляпы и т.д.'
        ),
        to='CategoryBase',
        on_delete=models.PROTECT,
    )

    class Meta:
        """Model settings"""

        ordering = (
            core.models.BaseCreature.created.field.name,
            core.models.BaseCreature.name.field.name,
        )


class CategoryBase(core.models.BaseCreature):
    """
    category model for items category
    describes item base category: hoodie -> top wear,
    pants -> bottom wear and other.

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    """

    class Meta:
        """Model settings"""

        ordering = (
            core.models.BaseCreature.created.field.name,
            core.models.BaseCreature.name.field.name,
        )


class OrderCustom(models.Model):
    """
    order model
    describes user`s order

    user: id FK -> auth.User
    max_price: integer. User`s budget
    header: char[100]. Short essence of order
    text: Task for designer
    status: char[4]. Choices
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    designer: id FK -> auth.User.
    """

    process_choices = (
        ('wait', 'в обработке'),
        ('got', 'принят'),
        ('proc', 'в процессе'),
        ('deli', 'в доставке'),
        ('done', 'выполнен'),
    )

    user: Union[
        'auth.models.User', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        to='user_auth.User',
        verbose_name='заказчик',
        related_name='user',
        help_text='Пользователь, оформивший заказ',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    max_price: Union[
        int, 'models.IntegerField[Any, Any]'
    ] = models.IntegerField(
        verbose_name='максимальная сумма заказа',
        help_text='Бюджет пользователя',
    )
    header: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
        verbose_name='заголовок',
        help_text='Заголовок заказа',
        max_length=100,
        blank=False,
        null=False,
    )
    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='описание стиля',
        help_text='Опишите стиль, добавьте интересные факты',
        blank=True,
        null=True,
    )
    status: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
        verbose_name='заголовок',
        help_text='Заголовок заказа',
        default=process_choices[0][0],
        choices=process_choices,
        max_length=4,
        blank=False,
        null=False,
    )
    designer: Union[
        'auth.models.User', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        to='user_auth.User',
        verbose_name='дизайнер',
        related_name='designer',
        help_text='Дизайнер, получивший заказ',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
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


class OrderPicture(models.Model):
    """
    order model
    describes user`s order

    picture: image.
    order: id FK -> OrderCustom
    """

    picture: Union['models.ImageField[Any, Any]',] = models.ImageField(
        verbose_name='изображение',
        help_text='Изображение желаемого дизайна',
        upload_to='media/uploads/order_pictures',
    )
    order: Union[
        'OrderCustom', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        OrderCustom,
        verbose_name='заказ',
        help_text='Номер заказа',
        on_delete=models.CASCADE,
    )

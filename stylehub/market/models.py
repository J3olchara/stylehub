"""Market models"""
from typing import Any, Union

from django.db import models

import utils.functions
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

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
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

    category_base: Union[
        'CategoryBase', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
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


class Collection(core.models.BaseCreature):
    """
    category model for items collection
    describes item base collection: Haute Couture for example

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    style: ManyToManyField market.models.Style
    text: TextField - collection description
    designer: ForeignKey - to user_auth.User
    """

    style: Union[
        models.query.QuerySet[Style],
        'models.ManyToManyField[Any, Any]',
    ] = models.ManyToManyField(Style, verbose_name='стиль коллекции')

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='описание коллекции'
    )

    designer: Union[Any, 'models.ForeignKey[Any, Any]',] = models.ForeignKey(
        to='user_auth.User',
        on_delete=models.CASCADE,
        verbose_name='дизайнер коллекции',
        help_text='Укажите кто создал эту коллекцию',
    )


class Item(core.models.BaseCreature):
    """
    Item models

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    designer: ForeignKey to auth.models.designer
    main_image: ImageField - image to describe main idea of item
    cost: PositiveBigIntegerField - describe how many this item cost
    text: TextField - item description
    category: ForeignKey to market.models.Category
    styles: ManyToManyField market.models.Style
    collection: ManyToOneField(ForeignKey) market.models.Collection

    """

    designer: Union[
        Any,
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)

    main_image: Union[Any, 'models.ImageField'] = models.ImageField(
        verbose_name='основная картинка товара',
        upload_to=utils.functions.get_upload_location,
        null=True,
        blank=True,
    )

    cost: Union[
        int, 'models.PositiveBigIntegerField[Any, Any]'
    ] = models.PositiveBigIntegerField(
        verbose_name='стоимость товара',
        help_text='добавьте стоимость вашего товара',
    )

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='описание товара',
        help_text='опишите ваш товар',
        null=True,
        blank=True,
    )

    category: Union[
        models.query.QuerySet[CategoryExtended],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=CategoryExtended,
        on_delete=models.CASCADE,
        verbose_name='категория товара',
        help_text='указывает на категорию, к которой относится товар',
    )

    styles: Union[
        models.query.QuerySet[Style],
        'models.ManyToManyField[Any, Any]',
    ] = models.ManyToManyField(
        to=Style,
        verbose_name='стиль товара',
        help_text='указывает к какому стилю принадлежит товар',
    )

    collection: Union[
        models.query.QuerySet[Collection],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        verbose_name='коллекции, в которых есть этот товар',
        help_text='показывает участвует ли товар в каких-либо коллекциях',
    )


class ItemPicture(models.Model):
    """
    models realise pictures gallery for item
    picture: ImageField one of many item picture
    item: ManyToManyField shows for what item this picture
    """

    picture: Union[Any, 'models.ImageField'] = models.ImageField(
        verbose_name='изображение',
        help_text='изображение для галерии товара',
        upload_to=utils.functions.get_upload_location,
    )

    item: Union[
        models.query.QuerySet[Item],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='галерея изображений товара',
        help_text='добавьте как можно болеее информативные фотографии',
    )

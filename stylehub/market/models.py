"""Market models"""
from typing import Any, Union

from django.db import models

import core.models
import market.utils


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

    style = models.ManyToManyField(Style, verbose_name='стиль коллекции')

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='описание коллекции'
    )

    designer = models.ForeignKey(
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

    designer = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)

    main_image = models.ImageField(
        verbose_name='основная картинка товара',
        upload_to=market.utils.get_upload_location,
        null=True,
        blank=True,
    )

    cost = models.PositiveBigIntegerField(
        verbose_name='стоимость товара',
        help_text='добавьте стоимость вашего товара',
    )

    text = models.TextField(
        verbose_name='описание товара',
        help_text='опишите ваш товар',
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        to=CategoryExtended,
        on_delete=models.CASCADE,
        verbose_name='категория товара',
        help_text='указывает на категорию, к которой относится товар',
    )

    styles = models.ManyToManyField(
        to=Style,
        verbose_name='стиль товара',
        help_text='указывает к какому стилю принадлежит товар',
    )

    collection = models.ForeignKey(
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

    picture = models.ImageField(verbose_name='изображение', help_text='')

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='галерея изображений товара',
        help_text='добавьте как можно болеее информативные фотографии',
    )


class Cart(core.models.CreatedEdited):
    """
    User cart to stash chosen items

    created: datetime. creation datetime
    edited: datetime. editing datetime
    items: QuerySet[market.models.Item]. chosen items
    """
    items = models.ManyToManyField(
        verbose_name='предметы в корзине',
        help_text='Предметы, которые пользователь добавил в корзину',
        to='Item',
    )

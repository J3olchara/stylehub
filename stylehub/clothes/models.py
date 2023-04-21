"""Market models"""
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup

import auth.models
import clothes.managers
import core.models
import market.models


@cleanup.select
class OrderClothes(market.models.Order):
    """
    OrderClothes model to store item buyings

    user: FK.
    designer: FK.
    sum: int. order cost
    item: FK
    status: choces statuses. order status
    created: datetime. creation datetime
    edited: editing datetime
    """

    objects = clothes.managers.OrderClothesManager()

    user = models.ForeignKey(
        verbose_name=_('заказчик'),
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_clothes_user',
    )

    designer = models.ForeignKey(
        verbose_name=_('исполнитель'),
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_clothes_designer',
    )

    sum = models.IntegerField(
        verbose_name=_('общая стоимость заказа'),
        null=False,
        blank=False,
    )
    item = models.ForeignKey(
        to='Item', on_delete=models.PROTECT, verbose_name=_('заказанная вещь')
    )

    class Meta:
        """Model settings"""

        verbose_name = _('заказ одежды')
        verbose_name_plural = _('заказы одежды')


@cleanup.select
class Collection(core.models.MainImageMixin, core.models.CreatedEdited):
    """
    category model for items collection
    describes item base collection: Haute Couture for example

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    styles: ManyToManyField market.models.Style
    text: TextField - collection description
    designer: ForeignKey - to user_auth.User
    """

    objects = clothes.managers.CollectionManager()

    styles = models.ManyToManyField(
        market.models.Style,
        verbose_name=_('стиль коллекции'),
        related_name='item_styles',
    )

    name = models.CharField(
        verbose_name=_('название коллекции'),
        max_length=100,
    )

    text = models.TextField(verbose_name=_('описание коллекции'))

    designer = models.ForeignKey(
        to='user_auth.User',
        on_delete=models.CASCADE,
        verbose_name=_('дизайнер коллекции'),
        help_text=_('Укажите кто создал эту коллекцию'),
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        for item in Item.objects.pref_styles().filter(collection=self):
            for style in item.styles.all():
                if style not in self.styles.all():
                    self.styles.add(style)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        """Model settings"""

        verbose_name = _('коллекция')
        verbose_name_plural = _('коллекции')


@cleanup.select
class Item(core.models.MainImageMixin, core.models.CreatedEdited):
    """
    Item models

    name: char[50]. Item name.
    designer: ForeignKey to auth.models.designer
    image: ImageField - image to describe main idea of item
    cost: PositiveBigIntegerField - describe how many this item cost
    text: TextField - item description
    category: ForeignKey to market.models.Category
    styles: ManyToManyField market.models.Style
    collection: ManyToOneField(ForeignKey) market.models.Collection
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.

    """

    objects = clothes.managers.ItemManager()

    item_genders = (
        ('male', _('Мужской')),
        ('female', _('Женский')),
        ('unisex', _('Унисекс')),
        ('childish', _('Детский')),
    )

    name = models.CharField(
        verbose_name=_('Название товара'),
        help_text=_(
            'Придумайте не длинное название, передающее основные черты товара'
        ),
        max_length=50,
    )

    designer = models.ForeignKey(
        verbose_name=_('дизайнер вещи'),
        related_name='item_designer',
        to='user_auth.User',
        on_delete=models.CASCADE,
    )

    gender = models.CharField(
        verbose_name=_('пол'),
        help_text=_('Кто будет носить эту вещь?'),
        choices=item_genders,
        default=item_genders[2][0],
        max_length=15,
        blank=False,
        null=False,
    )

    cost = models.IntegerField(
        verbose_name=_('стоимость товара'),
        help_text=_('добавьте стоимость вашего товара'),
    )

    text = models.TextField(
        verbose_name=_('описание товара'),
        help_text=_('опишите ваш товар'),
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        related_name='item_category',
        to=market.models.CategoryExtended,
        on_delete=models.CASCADE,
        verbose_name=_('категория товара'),
        help_text=_('указывает на категорию, к которой относится товар'),
    )

    styles = models.ManyToManyField(
        related_name='style',
        to=market.models.Style,
        verbose_name=_('стиль товара'),
        help_text=_('указывает к какому стилю принадлежит товар'),
    )

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        verbose_name=_('коллекция, в которой есть этот товар'),
        help_text=_('показывает участвует ли товар в каких-либо коллекциях'),
        related_name='items',
    )

    bought = models.IntegerField(
        verbose_name=_('куплено раз'),
        help_text=_('сколько раз купили этот товар'),
        default=0,
    )

    is_published = models.BooleanField(
        verbose_name='опубликован?',
        default=True,
    )

    def __str__(self) -> str:
        return self.name

    def buy(self, user: 'auth.models.User') -> OrderClothes:
        """creates an order with item and increments bought count"""
        self.bought += 1
        self.save()
        return OrderClothes.objects.create(
            user=user,
            designer=self.designer,
            sum=self.cost,
            item=self,
        )

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save()
        self.collection.save()

    class Meta:
        """Model settings"""

        verbose_name = _('вещь')
        verbose_name_plural = _('вещи')


Item._meta.get_field('image').default = 'defaults/item.png'


@cleanup.select
class ItemPicture(core.models.MainImageMixin):
    """
    models realise pictures gallery for item
    picture: ImageField one of many item picture
    item: ManyToOne shows for what item this picture
    """

    objects = clothes.managers.ItemPictureManager()
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name=_('галерея изображений товара'),
        help_text=_('добавьте как можно болеее информативные фотографии'),
        related_name='images',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('фотография вещи')
        verbose_name_plural = _('фотографии вещей')


class Evaluation(market.models.Evaluation):
    """
    Evalution on items from users

    created: datetime. creation datetime
    edited: datetime. editing datetime
    user: QuerySet[auth.models.User]. User who evaluated Item.
    item: QuerySet[market.models.Item]. Item for Evaluation
    rating: models.PositiveSmallIntegerField(int) Rating of evaluation
            from EVALUATION_VALUE_CHOICES
    goods: models.TextField(str) Good sides of Item
    negatives: models.TextField(str) Bad sides of Item
    text: models.TextField(str) Evaluation description
    """

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name=_('товар'),
        help_text=_('товар, к которому оставили отзыв'),
        related_name='evaluations',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

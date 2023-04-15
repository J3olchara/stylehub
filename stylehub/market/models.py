"""Market models"""
from typing import Any, Union

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

import core.models
import market.managers
import utils.functions


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

        verbose_name = _('стиль')
        verbose_name_plural = _('стили')

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

        verbose_name = _('категория одежды')
        verbose_name_plural = _('категории одежды')

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

        verbose_name = _('тип одежды')
        verbose_name_plural = _('типы одежды')

        ordering = (
            core.models.BaseCreature.created.field.name,
            core.models.BaseCreature.name.field.name,
        )


class OrderCustom(core.models.CreatedEdited):
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

    user = models.ForeignKey(
        to='user_auth.User',
        verbose_name='заказчик',
        related_name='user',
        help_text='Пользователь, оформивший заказ',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )
    max_price = models.IntegerField(
        verbose_name='максимальная сумма заказа',
        help_text='Бюджет пользователя',
    )
    header = models.CharField(
        verbose_name='заголовок',
        help_text='Заголовок заказа',
        max_length=100,
        blank=False,
        null=False,
    )
    text = models.TextField(
        verbose_name='описание стиля',
        help_text='Опишите стиль, добавьте интересные факты',
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='заголовок',
        help_text='Заголовок заказа',
        default=process_choices[0][0],
        choices=process_choices,
        max_length=4,
        blank=False,
        null=False,
    )
    designer = models.ForeignKey(
        to='user_auth.User',
        verbose_name='дизайнер',
        related_name='designer',
        help_text='Дизайнер, получивший заказ',
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )

    class Meta:
        """Model settings"""

        verbose_name = _('заказ кастома')
        verbose_name_plural = _('заказы кастомов')


class OrderPicture(models.Model):
    """
    order model
    describes user`s order

    picture: image.
    order: id FK -> OrderCustom
    """

    picture: Union[Any, 'models.ImageField'] = models.ImageField(
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

    class Meta:
        """Model settings"""

        verbose_name = _('фотография заказа кастома')
        verbose_name_plural = _('фотографии заказов кастомов')


class Collection(core.models.CreatedEdited):
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

    objects = market.managers.CollectionManager()

    style = models.ManyToManyField(Style, verbose_name='стиль коллекции')

    name = models.CharField(
        verbose_name='Название коллекции',
        max_length=100,
    )

    text = models.TextField(verbose_name='описание коллекции')

    designer = models.ForeignKey(
        to='user_auth.User',
        on_delete=models.CASCADE,
        verbose_name='дизайнер коллекции',
        help_text='Укажите кто создал эту коллекцию',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        """Model settings"""

        verbose_name = _('коллекция')
        verbose_name_plural = _('коллекции')


class Item(core.models.CreatedEdited):
    """
    Item models

    name: char[50]. Item name.
    designer: ForeignKey to auth.models.designer
    main_image: ImageField - image to describe main idea of item
    cost: PositiveBigIntegerField - describe how many this item cost
    text: TextField - item description
    category: ForeignKey to market.models.Category
    styles: ManyToManyField market.models.Style
    collection: ManyToOneField(ForeignKey) market.models.Collection
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.

    """

    name = models.CharField(
        verbose_name=_('Название товара'),
        help_text=_(
            'Придумайте не длинное название, передающее основные черты товара'
        ),
        max_length=50,
    )
    designer = models.ForeignKey(
        verbose_name=_('Дизайнер вещи'),
        related_name='item_designer',
        to='user_auth.User',
        on_delete=models.CASCADE,
    )

    main_image = models.ImageField(
        verbose_name=_('основная картинка товара'),
        upload_to=utils.functions.get_item_main_image_location,
        null=True,
        blank=True,
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
        to=CategoryExtended,
        on_delete=models.CASCADE,
        verbose_name=_('категория товара'),
        help_text=_('указывает на категорию, к которой относится товар'),
    )

    styles = models.ManyToManyField(
        related_name='style',
        to=Style,
        verbose_name=_('стиль товара'),
        help_text=_('указывает к какому стилю принадлежит товар'),
    )

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        verbose_name='коллекция, в которой есть этот товар',
        help_text='показывает участвует ли товар в каких-либо коллекциях',
        related_name='items',
    )

    is_published = models.BooleanField(
        verbose_name='Опубликован?',
        default=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        """Model settings"""

        verbose_name = _('вещь')
        verbose_name_plural = _('вещи')


class ItemPicture(models.Model):
    """
    models realise pictures gallery for item
    picture: ImageField one of many item picture
    item: ManyToManyField shows for what item this picture
    """

    picture = models.ImageField(
        verbose_name='изображение',
        help_text='изображение для галерии товара',
        upload_to=utils.functions.get_item_images_upload_location,
    )

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='галерея изображений товара',
        help_text='добавьте как можно болеее информативные фотографии',
        related_name='images',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('фотография вещи')
        verbose_name_plural = _('фотографии вещей')


class OrderClothes(core.models.CreatedEdited):
    """
    OrderClothes model to store item buyings

    user: FK.
    designer: FK.
    sum: int. order cost
    item: FK
    status: choces statuses. order status
    """

    statuses = (
        ('0', 'Ожидает'),
        ('1', 'Принят'),
        ('2', 'в процессе'),
        ('3', 'доставка'),
        ('4', 'выполнен'),
    )

    user = models.ForeignKey(
        related_name='order_user',
        verbose_name='заказчик',
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    designer = models.ForeignKey(
        related_name='order_designer',
        verbose_name='исполнитель',
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    sum = models.IntegerField(
        verbose_name='общая стоимость заказа',
        null=False,
        blank=False,
    )
    item = models.ForeignKey(
        to='Item', on_delete=models.PROTECT, verbose_name='Заказанная вещь'
    )
    status = models.CharField(
        max_length=127,
        choices=statuses,
        default='0',
        blank=False,
        null=False,
    )

    class Meta:
        """Model settings"""

        verbose_name = _('заказ одежды')
        verbose_name_plural = _('заказы одежды')


class Cart(core.models.CreatedEdited):
    """
    User cart to stash chosen items

    created: datetime. creation datetime
    edited: datetime. editing datetime
    items: QuerySet[market.models.Item]. chosen items
    """

    user = models.OneToOneField(
        verbose_name='пользователь',
        to='user_auth.User',
        on_delete=models.CASCADE,
    )

    items = models.ManyToManyField(
        verbose_name='предметы в корзине',
        help_text='Предметы, которые пользователь добавил в корзину',
        to='Item',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')


class Evaluation(core.models.CreatedEdited):
    """
    Evalution on items from users

    created: datetime. creation datetime
    edited: datetime. editing datetime
    user: QuerySet[auth.models.User]. User who evaluated Item
    item: QuerySet[market.models.Item]. Item for Evaluation
    rating: models.PositiveSmallIntegerField(int) Rating of evaluation
            from EVALUATION_VALUE_CHOICES
    goods: models.TextField(str) Good sides of Item
    negatives: models.TextField(str) Bad sides of Item
    text: models.TextField(str) Evaluation description
    """

    EXCELLENT: int = 5
    GOOD: int = 4
    COMMON: int = 3
    BAD: int = 2
    TERRIBLE: int = 1
    EVALUATION_VALUE_CHOICES = (
        (EXCELLENT, 'Отличный товар'),
        (GOOD, 'Хороший товар'),
        (COMMON, 'Обычный товар'),
        (BAD, 'Плохой товар'),
        (TERRIBLE, 'Ужасный товар'),
    )

    user = models.ForeignKey(
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluations',
        verbose_name='пользователь',
        help_text='пользователь, оставивший отзыв',
    )

    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='товар',
        help_text='товар, к которому оставили отзыв',
        related_name='rating_item',
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(
                5, message='Максимальное значение оценки - 5'
            ),
            validators.MinValueValidator(
                1, message='Минимальное значение оценки - 1'
            ),
        ],
        choices=EVALUATION_VALUE_CHOICES,
        verbose_name='оценка товара',
        help_text='Ваша оценка',
    )

    goods = models.TextField(
        verbose_name='Достоинства',
        help_text='Какие позитивные стороны вы нашли у этого товара',
        blank=True,
        null=True,
    )

    negatives = models.TextField(
        verbose_name='Недостатки',
        help_text='Какие недостатки вы нашли у этого товара',
        blank=True,
        null=True,
    )

    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Ваш комментарий после использования этого товара',
        blank=True,
        null=True,
    )

    class Meta:
        """Model settings"""

        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

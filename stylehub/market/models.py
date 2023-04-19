"""Market models"""
from typing import Any, Union

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

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


class OrderPicture(models.Model):
    """
    order model
    describes user`s order

    picture: image.
    order: id FK -> OrderCustom
    """

    picture = models.ImageField(
        verbose_name='изображение',
        help_text='Изображение желаемого дизайна',
        upload_to='uploads/order_pictures',
    )

    class Meta:
        """Model settings"""

        abstract = True


class Order(core.models.CreatedEdited):
    """
    Order model to store item buyings

    user: FK.
    designer: FK.
    status: choces statuses. order status
    """

    statuses = (
        ('wait', 'Ожидает'),
        ('got', 'Принят'),
        ('proc', 'в процессе'),
        ('deli', 'доставка'),
        ('done', 'выполнен'),
    )

    user = models.ForeignKey(
        verbose_name='заказчик',
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    designer = models.ForeignKey(
        verbose_name='исполнитель',
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        max_length=127,
        choices=statuses,
        default='wait',
        blank=False,
        null=False,
    )

    class Meta:
        """Model settings"""

        abstract = True

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
        to='clothes.Item',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')


class Evaluation(core.models.CreatedEdited):
    """
    Evalution abstract model

    created: datetime. creation datetime
    edited: datetime. editing datetime
    user: QuerySet[auth.models.User]. User that evaluated
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
        verbose_name='оценка',
        help_text='Ваша оценка',
    )

    goods = models.TextField(
        verbose_name='Достоинства',
        blank=True,
        null=True,
    )

    negatives = models.TextField(
        verbose_name='Недостатки',
        blank=True,
        null=True,
    )

    text = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )

    class Meta:
        """Model settings"""

        abstract = True

        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

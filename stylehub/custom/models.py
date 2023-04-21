"""Market models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup

import custom.managers
import market.models


class OrderCustom(market.models.Order):
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

    objects = custom.managers.OrdersManager()

    user = models.ForeignKey(
        verbose_name=_('заказчик'),
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_custom_user',
    )

    designer = models.ForeignKey(
        verbose_name=_('исполнитель'),
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_custom_designer',
    )

    max_price = models.IntegerField(
        verbose_name=_('максимальная сумма заказа'),
        help_text=_('Бюджет пользователя'),
    )

    header = models.CharField(
        verbose_name=_('заголовок'),
        help_text=_('Заголовок заказа'),
        max_length=100,
        blank=False,
        null=False,
    )

    text = models.TextField(
        verbose_name=_('описание желаемого дизайна'),
        help_text=_(
            'Опишите дизайн, добавьте какие-то идеи '
            'к выбранному изображению'
        ),
        blank=True,
        null=True,
    )

    class Meta:
        """Model settings"""

        verbose_name = _('заказ кастома')
        verbose_name_plural = _('заказы кастомов')


@cleanup.select
class OrderCustomPicture(market.models.OrderPicture):
    """
    order model
    describes user`s order

    picture: image.
    order: id FK -> OrderCustom
    """

    order = models.ForeignKey(
        'OrderCustom',
        verbose_name=_('заказ'),
        help_text=_('Номер заказа'),
        on_delete=models.CASCADE,
    )

    class Meta:
        """model settings"""

        verbose_name = _('фотография заказа кастома')
        verbose_name_plural = _('фотографии заказов кастомов')


class OrderCustomEvaluation(market.models.Evaluation):
    """
    Evalution on items from users

    created: datetime. creation datetime
    edited: datetime. editing datetime
    user: QuerySet[auth.models.User]. User who evaluated Item.
    order: QuerySet[custom.models.OrderCustom]. OrderCustom for Evaluation
    rating: models.PositiveSmallIntegerField(int) Rating of evaluation
            from EVALUATION_VALUE_CHOICES
    goods: models.TextField(str) Good sides of Item
    negatives: models.TextField(str) Bad sides of Item
    text: models.TextField(str) Evaluation description
    """

    user = models.ForeignKey(
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='custom_evaluations',
        verbose_name=_('пользователь'),
        help_text=_('пользователь, оставивший отзыв'),
    )

    order = models.ForeignKey(
        to=OrderCustom,
        on_delete=models.CASCADE,
        verbose_name=_('заказ'),
        help_text=_('заказ, к которому оставили отзыв'),
        related_name='evaluations',
    )

    class Meta:
        """Model settings"""

        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

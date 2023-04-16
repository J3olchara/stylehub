"""Market models"""
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    user = models.ForeignKey(
        verbose_name='заказчик',
        to='user_auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_custom_user',
    )

    designer = models.ForeignKey(
        verbose_name='исполнитель',
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


class OrderCustomPicture(market.models.OrderPicture):
    """
    order model
    describes user`s order

    picture: image.
    order: id FK -> OrderCustom
    """

    order = models.ForeignKey(
        'OrderCustom',
        verbose_name='заказ',
        help_text='Номер заказа',
        on_delete=models.CASCADE,
    )

    class Meta:
        """model settings"""

        verbose_name = _('фотография заказа кастома')
        verbose_name_plural = _('фотографии заказов кастомов')

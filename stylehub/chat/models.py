"""models for chat"""

from datetime import datetime
from typing import Any, Union

from django.db import models
from django.utils.translation import gettext_lazy as _

import auth.models
import utils.functions


class Messages(models.Model):
    """
    Messages model shows informations about messages

    user: auth.models.User. From/to which User.
    designer: auth.models.User. From/to which designer.
    image: ImageField. If ypu have addition as picrure in message it will be
                       here
    message: TextField. Text value of message
    created: DateTimeField. When message have been created
    """

    user: Union[
        models.query.QuerySet[auth.models.User],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=auth.models.User,
        on_delete=models.CASCADE,
        verbose_name=_('пользователь отправивший сообщение'),
        help_text=_('какому пользователю принадлежит сообщение'),
        related_name='users_messages',
    )

    designer: Union[
        models.query.QuerySet[auth.models.User],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=auth.models.User,
        on_delete=models.CASCADE,
        verbose_name=_('дизайнер отправивший сообщение'),
        help_text=_('какому дизайнеру принадлежит сообщение'),
        related_name='designers_messgaes',
    )

    image: Union[Any, 'models.ImageField'] = models.ImageField(
        verbose_name=_('приложение к сообщению'),
        help_text=_('Приложите свое вложение к сообщению'),
        upload_to=utils.functions.get_message_image_upload_location,
        null=True,
        blank=True,
    )

    message: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name=_('текст сообщения'),
        help_text=_('введите текст сообщения'),
    )

    created: Union[
        datetime, 'models.DateTimeField[Any, Any]'
    ] = models.DateTimeField(
        verbose_name=_('дата и время создания'),
        help_text=_('Автоматически выставляется при создании'),
        auto_now_add=True,
        blank=False,
        null=False,
    )

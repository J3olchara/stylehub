"""models for chat"""

from datetime import datetime
from typing import Any, Union

from django.db import models

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
        on_delete=models.SET_NULL,
        verbose_name='пользователь отправивший сообщение',
        help_text='какому пользователю принадлежит сообщение',
    )

    designer: Union[
        models.query.QuerySet[auth.models.User],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        to=auth.models.User,
        on_delete=models.SET_NULL,
        verbose_name='дизайнер отправивший сообщение',
        help_text='какому дизайнеру принадлежит сообщение',
    )

    image: Union[Any, 'models.ImageField'] = models.ImageField(
        verbose_name='Приложение к сообщению',
        help_text='Приложите свое вложение к сообщению',
        upload_to=utils.functions.get_upload_location,
        null=True,
        blank=True,
    )

    message: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='текст сообщения',
        help_text='введите текст сообщения',
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

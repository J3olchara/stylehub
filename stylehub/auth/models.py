"""models for auth"""
from typing import Any, Union

from django.contrib.auth.models import AbstractUser
from django.db import models

import market.models


class User(AbstractUser):
    """
    Extended User model from AbstractUser

    last_category: market.models.Category. Last seen user category.
    last_styles: market.models.category[:5]. Five last seen styles.
    is_designer: bool. user is designer?
    """

    last_category: Union[
        models.query.QuerySet[market.models.CategoryExtended],
        'models.ForeignKey[Any, Any]',
    ] = models.ForeignKey(
        verbose_name='последняя посещённая категория',
        to=market.models.CategoryExtended,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    last_styles: Union[
        models.query.QuerySet[market.models.Style],
        'models.ManyToManyField[Any, Any]',
    ] = models.ManyToManyField(
        verbose_name='последние пять посещённых стилей',
        to=market.models.Style,
        blank=True,
    )

    is_designer: 'models.BooleanField[Union[bool, Any], bool]' = (
        models.BooleanField(
            verbose_name='пользователь дизайнер?',
            help_text='Отвечает на вопрос, пользователь является '
            'дизайнером или нет?',
            default=False,
        )
    )

    def clean(self) -> None:
        if self.last_styles.count() > 5:
            self.last_styles = self.last_styles[-5:]
        return super().clean()


class DesignerProfile(models.Model):
    """
    This model correspond Designers

    user: User key, shows with what user related designer
    avatar: models.ImageField - Image, which shows on designers avatar
    background: models.ImageField - Image, which users see on background
                designer profile
    text: models.TextField - Textfield where is designer write information
          about himself
    balance: models.IntegerField - Int value, which shows how many money our
             site owe to designer
    """

    user: Union[User, 'models.OneToOneField[Any, Any]'] = models.OneToOneField(
        to=User, on_delete=models.CASCADE
    )

    avatar: 'models.ImageField' = models.ImageField(
        verbose_name='аватарка дизайнера',
        upload_to='designers/avatars',
        null=True,
        blank=True,
    )

    backgroound: 'models.ImageField' = models.ImageField(
        verbose_name='картинка на заднем фоне в профиле дизайнера',
        upload_to='designers/backgrounds',
        null=True,
        blank=True,
    )

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name='информация о дизайнере',
        help_text='введите информацию о себе',
        blank=True,
        null=True,
    )
    balance: Union[int, 'models.IntegerField[Any, Any]'] = models.IntegerField(
        verbose_name='знаечение баланса дизайнера', default=0
    )

    class Meta:
        """settings for DesignerProfile"""

        verbose_name = 'дизайнер'
        verbose_name_plural = 'дизайнеры'

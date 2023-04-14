"""models for auth"""
from typing import Any, Optional, Sequence, Union

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as UserManagerOld
from django.db import models
from django.db.models.expressions import Combinable
from django.utils.translation import gettext_lazy as _

import market.models


class UserManager(UserManagerOld[AbstractUser]):
    """
    User manager

    Write your custom objects methods here
    """

    def create_user(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> AbstractUser:
        """
        extended user creating

        creates cart for user
        """
        cart = market.models.Cart.objects.create()
        return super().create_user(
            username, email, password, cart=cart, **extra_fields
        )

    def create_superuser(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any
    ) -> AbstractUser:
        """
        extended superuser creating

        creates cart for superuser
        """
        cart = market.models.Cart.objects.create()
        return super().create_superuser(
            username, email, password, cart=cart, **extra_fields
        )


class User(AbstractUser):
    """
    Extended User model from AbstractUser

    last_category: market.models.Category. Last seen user category.
    last_styles: market.models.category[:5]. Five last seen styles.
    is_designer: bool. user is designer?
    """

    objects = UserManager()

    gender_choices = (
        ('', _('Не указан')),
        ('male', _('Мужской')),
        ('female', _('Женский')),
    )

    gender: (
        'models.CharField[Union[str, int, Combinable], str]'
    ) = models.CharField(
        verbose_name=_('пол'),
        help_text=_('Укажите ваш пол'),
        choices=gender_choices,
        max_length=127,
        default='',
        blank=True,
    )

    email: (
        'models.EmailField[Union[str, int, Combinable], str]'
    ) = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )

    last_category: (
        'models.ForeignKey[Union[market.models.CategoryExtended, '
        'Combinable, None], '
        'Optional[market.models.CategoryExtended]]'
    ) = models.ForeignKey(
        verbose_name=_('последняя посещённая категория'),
        to=market.models.CategoryExtended,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    last_styles: (
        'models.ManyToManyField[Sequence[market.models.Style], '
        'models.manager.RelatedManager[market.models.Style]]'
    ) = models.ManyToManyField(
        verbose_name=_('последние пять посещённых стилей'),
        to=market.models.Style,
        blank=True,
    )

    is_designer: (
        'models.BooleanField[Union[bool, Combinable], bool]'
    ) = models.BooleanField(
        verbose_name=_('пользователь дизайнер?'),
        help_text=_(
            'Отвечает на вопрос, пользователь является дизайнером или нет?'
        ),
        default=False,
    )

    def clean(self) -> None:
        if self.last_styles.count() > 5:
            to_remove = self.last_styles.order_by('?').last()
            self.last_styles.remove(self.last_styles.get(to_remove))
            self.save()
        return super().clean()

    def make_designer(self) -> 'DesignerProfile':
        """makes user designer"""
        self.is_designer = True
        self.full_clean()
        self.save()
        return DesignerProfile.objects.create(user=self)


class DesignerProfile(models.Model):
    """
    This model correspond Designers

    user: User key, shows with what user related designer
    avatar: models.ImageField - Image, which shows on designers avatar
    background: models.ImageField - Image, which users see on background
                designer profile
    text: models.TextField - Textfield where is designer write information
          about himself
    balance: models.IntegerField - Int value, which shows how much money our
             site owe to designer
    """

    user: Union[User, 'models.OneToOneField[Any, Any]'] = models.OneToOneField(
        to=User, on_delete=models.CASCADE
    )

    avatar: 'models.ImageField' = models.ImageField(
        verbose_name=_('аватарка дизайнера'),
        upload_to='designers/avatars',
        null=True,
        blank=True,
    )

    background: 'models.ImageField' = models.ImageField(
        verbose_name=_('картинка на заднем фоне в профиле дизайнера'),
        upload_to='designers/backgrounds',
        null=True,
        blank=True,
    )

    text: Union[str, 'models.TextField[Any, Any]'] = models.TextField(
        verbose_name=_('информация о дизайнере'),
        help_text=_('введите информацию о себе'),
        blank=True,
        null=True,
    )

    balance: Union[int, 'models.IntegerField[Any, Any]'] = models.IntegerField(
        verbose_name=_('баланс дизайнера'), default=0
    )

    class Meta:
        """settings for DesignerProfile"""

        verbose_name = _('дизайнер')
        verbose_name_plural = _('дизайнеры')

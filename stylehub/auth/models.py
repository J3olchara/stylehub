"""models for auth"""
import uuid
from datetime import datetime
from typing import Any, Optional, Sequence, Union

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import Combinable
from django.template.defaultfilters import strip_tags
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup
from pytz import timezone, utc

import auth.managers
import auth.utils
import clothes.models
import market.models


class User(AbstractUser):
    """
    Extended User model from AbstractUser

    last_category: market.models.Category. Last seen user category.
    last_styles: market.models.category[:5]. Five last seen styles.
    is_designer: bool. user is designer?
    """

    objects = auth.managers.UserManager()

    designers = auth.managers.DesignerManager()

    inactive = auth.managers.InactiveUserManager()

    active = auth.managers.ActiveUsersManager()

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
        related_name='styles',
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

    saved = models.ManyToManyField(
        verbose_name=_('сохранённые пользователем вещи'),
        to=clothes.models.Item,
        related_name='saved_items',
    )

    lovely = models.ManyToManyField(
        verbose_name=_('любимые дизайнеры'),
        to='User',
        related_name='lovely_designers',
    )

    failed_attemps = models.IntegerField(
        verbose_name=_('неудачных попыток входа'), default=0
    )

    def clean(self) -> None:
        if self.id and self.last_styles.count() > 5:
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

    def normalize_email(self) -> str:
        """
        Normalizes email address
        Cuts out email tags and leads it to canonical name
        """
        name, domain = strip_tags(self.email).lower().split('@')
        domain = domain.replace('ya.ru', 'yandex.ru')
        if domain == 'gmail.com':
            name = name.replace('.', '')
        elif domain == 'yandex.ru':
            name = name.replace('.', '-')
        name = name.split('+', maxsplit=1)[0]
        self.normalized_email = '@'.join([name, domain])
        return self.normalized_email


@cleanup.select
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
        to=User, on_delete=models.PROTECT, related_name='designer_profile'
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


class ActivationToken(models.Model):
    """
    Activation token model.
    Stores activation tokens that allows new accounts to be activated.
    user: int FK -> User. User that attached to token.
    token: uuid.UUID. Unique token.
    expire: datetime. Token expiration datetime
    """

    user: Union[User, Any] = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('пользователь'),
    )

    token: Union[uuid.UUID, Any] = models.UUIDField(
        verbose_name=_('ключ активации'), default=uuid.uuid4
    )

    created: Union[datetime, Any] = models.DateTimeField(
        verbose_name=_('дата и время создания'),
        auto_now_add=True,
    )

    expire: Union[datetime, Any] = models.DateTimeField(
        verbose_name=_('дата и время истечения'),
        default=auth.utils.get_token_expire,
    )

    def __str__(self) -> str:
        return str(self.token)

    def get_url(self, site: str) -> Any:
        """returns activation url"""
        return site + reverse(
            'auth:signup_confirm',
            kwargs={'user_id': self.user.id, 'token': self.token},
        )

    def expired(self) -> bool:
        """Checks if the token has expired"""
        tz = timezone(settings.TIME_ZONE)
        expire = self.expire.replace(tzinfo=utc).astimezone(tz)
        exp = expire < datetime.now(tz=tz)
        if exp:
            self.delete()
        return exp

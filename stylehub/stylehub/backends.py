"""backends for project"""
from typing import Any, Optional, Type, Union

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from auth.models import AbstractUser, ActivationToken, User


class LoginBackend(ModelBackend):
    """modifed LoginBackend that can aunthenticate by email and username"""

    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Optional[AbstractUser], Any]:
        user_model = User
        user: Any = self.try_get(user_model, username=username)
        if not user:
            user = self.try_get(user_model, email__iexact=username)
        if user and password is not None:
            if user.check_password(password):
                return user
            user.failed_attemps += 1
            if user.failed_attemps >= settings.FAILED_AUTHS_TO_DEACTIVATE:
                self.send_freeze_mail(user)
                user.is_active = False
                user.save()
            user.save()
        return None

    @staticmethod
    def try_get(
        user_model: Type[User], **kwargs: Any
    ) -> Optional[AbstractUser]:
        """trying to get user without error"""
        try:
            user = user_model.objects.get(**kwargs)
            return user
        except user_model.DoesNotExist:
            return None

    @staticmethod
    def send_freeze_mail(user: User) -> None:
        """returns freezee email with activation url"""
        token = ActivationToken.objects.create(user=user)
        message = ''.join(
            (
                str(_('Дорогой ')),
                f'{user.username}',
                '!\n\n',
                str(
                    _(
                        'На вашем аккаунте обнаружена подозрительная '
                        'активность и нам пришлось его заморозить.\n'
                        'Чтобы снова получить доступ к своему '
                        'аккаунту перейдите по ссылке:\n'
                    )
                ),
                f'{token.get_url}',
            )
        )
        send_mail(
            subject=('Подозрительная активность на аккаунте!'),
            recipient_list=[user.email],
            from_email=settings.SITE_EMAIL,
            message=message,
        )

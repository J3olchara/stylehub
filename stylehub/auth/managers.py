"""Managers for auth models"""
from typing import Any, Optional, Union

from django.apps import apps
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.contrib.auth.models import UserManager as UserManagerOld
from django.db import models


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
        cart = apps.get_model('market', 'Cart')
        user = super().create_user(username, email, password, **extra_fields)
        cart.objects.create(user=user)
        return user

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
        superuser = super().create_superuser(
            username, email, password, **extra_fields
        )
        cart = apps.get_model('market', 'Cart')
        cart.objects.create(user=superuser)
        return superuser

    def get_lovely_designers(
        self, user: Union[AbstractUser, AnonymousUser]
    ) -> models.query.QuerySet[Any]:
        """Returns lovely designers of this user"""
        users = apps.get_model('user_auth', 'User')
        prefetch_designers = models.Prefetch(
            self.model.lovely.field.name,
            queryset=users.objects.filter(is_designer=True),
        )

        return (
            (
                self.get_queryset()
                .filter(pk=user.id)
                .prefetch_related(prefetch_designers)
            )
            .first()
            .lovely.all()
        )

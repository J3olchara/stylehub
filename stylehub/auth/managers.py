"""Managers for auth models"""
from typing import Any, Optional

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as UserManagerOld


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

"""Managers for auth models"""
from typing import Any, Optional

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as UserManagerOld
from django.db.models import QuerySet, aggregates
from django.db.models.functions import Coalesce


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
        **extra_fields: Any,
    ) -> AbstractUser:
        """
        extended user creating

        creates cart for user
        """
        cart: Any = apps.get_model('market', 'Cart')
        user = super().create_user(username, email, password, **extra_fields)
        cart.objects.create(user=user)
        return user

    def create_superuser(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> AbstractUser:
        """
        extended superuser creating

        creates cart for superuser
        """
        superuser = super().create_superuser(
            username, email, password, **extra_fields
        )
        cart: Any = apps.get_model('market', 'Cart')
        cart.objects.create(user=superuser)
        return superuser

    def get_queryset(self) -> QuerySet[AbstractUser]:
        """show only active users"""
        return super().get_queryset().filter(is_active=True)


class DesignerManager(UserManager):
    """manager to work with designers"""

    def create_superuser(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> AbstractUser:
        """
        creates user with designerprofile
        """
        superuser: Any = super().create_superuser(
            username, email, password, **extra_fields
        )
        superuser.make_designer()
        return superuser

    def create_user(
        self,
        username: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> AbstractUser:
        """
        creates superuser with designerprofile
        """
        user: Any = super().create_user(
            username, email, password, **extra_fields
        )
        user.make_designer()
        return user

    def get_queryset(self) -> QuerySet[AbstractUser]:
        return (
            super()
            .get_queryset()
            .select_related('designer_profile')
            .filter(is_designer=True)
        )

    def with_buys(self) -> QuerySet[AbstractUser]:
        """returns new queryset of designer users"""
        item: Any = apps.get_model('clothes', 'Item')
        return self.get_queryset().annotate(
            buys=Coalesce(
                aggregates.Sum(f'item_designer__{item.bought.field.name}'), 0
            ),
        )

    def top(self) -> QuerySet[Any]:
        """returns new queryset of top designer users"""
        return self.with_buys().order_by('-buys')

    def unpopular(self) -> QuerySet[AbstractUser]:
        """returns new queryset of unpopular designer users"""
        return (
            self.with_buys()
            .filter(buys__lt=settings.POPULAR_DESIGNER_BUYS)
            .order_by('buys')
        )

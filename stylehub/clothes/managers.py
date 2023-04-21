"""Managers for market models"""

from typing import Any, List, Union

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import Case, Value, When, aggregates

import auth.models


class ItemManager(models.Manager[Any]):
    """Item manager for Item model"""

    def get_details(self) -> models.QuerySet[Any]:
        """item with evaluations :return"""
        evaluations: Any = apps.get_model('clothes', 'Evaluation')
        item_picture: Any = apps.get_model('clothes', 'ItemPicture')
        prefetch_evals = models.Prefetch(
            'evaluations', evaluations.objects.all()
        )
        prefetch_gallery = models.Prefetch(
            'images', item_picture.objects.all()
        )
        return self.get_queryset().prefetch_related(
            prefetch_evals, prefetch_gallery
        )

    def pref_styles(self) -> models.QuerySet[Any]:
        """returns new queryset with prefetched item styles"""
        style: Any = apps.get_model('market', 'Style')
        return self.get_queryset().prefetch_related(
            models.Prefetch('styles', queryset=style.objects.all())
        )

    def unpopular(self) -> models.QuerySet[Any]:
        """returns random items with unpopular designers"""
        qs = self.get_queryset().filter(
            designer__in=auth.models.User.designers.unpopular().all()
        )
        return qs


class CollectionManager(models.Manager[Any]):
    """Manager for Collection model"""

    def with_items(self) -> models.query.QuerySet[Any]:
        """Returns Item, which belongs collection"""
        item: Any = apps.get_model('clothes', 'Item')
        style: Any = apps.get_model('market', 'Style')
        image: Any = apps.get_model('clothes', 'ItemPicture')
        prefetch_images = models.Prefetch(
            'images',
            queryset=image.objects.all().only(image.image.field.name),
        )
        item_queryset = (
            item.objects.filter(is_published=True)
            .select_related(item.category.field.name)
            .prefetch_related(prefetch_images)
        )

        prefetch_items = models.Prefetch('items', queryset=item_queryset)

        prefetch_styles = models.Prefetch(
            self.model.styles.field.name,
            queryset=style.objects.only(style.name.field.name),
        )
        return (
            self.get_queryset()
            .prefetch_related(prefetch_items)
            .prefetch_related(prefetch_styles)
        )

    def recommend(
        self, user: Union['auth.models.User', AnonymousUser]
    ) -> models.query.QuerySet[Any]:
        """return popular items based on user last seen styles"""
        item: Any = apps.get_model('clothes', 'Item')
        qs: models.query.QuerySet[Any] =  self.with_items()
        if user.is_authenticated and user.last_styles.count() >= 1:
            qs = qs.filter(styles__in=user.last_styles.all())
        return (
            qs.annotate(
                buys=aggregates.Sum(f'items__{item.bought.field.name}')
            )
            .filter(buys__gte=settings.POPULAR_COLLECTION_BUYS)
            .order_by('-buys')
        )

    def top(self) -> models.QuerySet[Any]:
        """returns top collections base on count items bought"""
        item: Any = apps.get_model('clothes', 'Item')
        return (
            self.with_items()
            .annotate(buys=aggregates.Sum(f'items__{item.bought.field.name}'))
            .filter(buys__gte=settings.POPULAR_COLLECTION_BUYS)
            .order_by('-buys')
        )


class OrderClothesManager(models.Manager[Any]):
    """Manager for OrderClothes model in clothes app"""

    def get_user_orders(
        self, user: Union['auth.models.User', AnonymousUser]
    ) -> models.QuerySet[Any]:
        """get users orders"""
        return (
            self.get_queryset()
            .filter(user=user)
            .select_related(self.model.item.field.name)
            .order_by(
                Case(When(status='done', then=Value(1)), default=Value(0)),
                f'-{self.model.edited.field.name}',
            )
        )


class ItemPictureManager(models.Manager[Any]):
    """Manager for ItemPicture in clothes app"""

    def create_many(self, images: List[UploadedFile], item: Any) -> List[Any]:
        """creates many than one objects simple"""
        objs = [self.model(image=image, item=item) for image in images]
        return self.bulk_create(objs)

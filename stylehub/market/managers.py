"""Managers for market models"""
from django.apps import apps
from django.db import models

import market


class ItemManager(models.Manager['market.models.Item']):
    """Item manager for Item model"""

    def get_details(self) -> models.QuerySet['market.models.Item']:
        """item with evaluations :return"""
        evaluations = apps.get_model('market', 'Evaluation')
        prefetch_evals = models.Prefetch(
            'evaluations', evaluations.objects.all()
        )
        return self.get_queryset().prefetch_related(prefetch_evals)

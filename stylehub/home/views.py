"""HOMEPAGE app pages views"""
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import HttpResponse
import django.views.generic
import clothes.models


class Home(django.views.generic.ListView):  # type: ignore[type-arg]
    """returns homepage"""

    template_name = 'home/index.html'
    context_object_name = 'items_raw'

    def get_queryset(self) -> QuerySet['clothes.models.Item']:
        return clothes.models.Item.objects.all()

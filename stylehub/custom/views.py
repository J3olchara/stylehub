"""Views of custom app"""
from typing import Any

from django.contrib.auth import mixins
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

import auth.mixins
import auth.models
import custom.models


class Main(mixins.LoginRequiredMixin, generic.ListView[Any]):
    """Main pagge of custom app"""

    template_name = 'custom/main.html'
    context_object_name = 'queryset'

    def get_queryset(self) -> QuerySet[Any]:
        """Returns queryset"""
        if self.request.user.is_designer:
            return custom.models.OrderCustom.objects.get_free_orders()
        print(auth.models.User.designers.best_custom_evaluations())
        return auth.models.User.designers.best_custom_evaluations()


class CustomDetail(
    auth.mixins.DesignerRequiredMixin,
    generic.DetailView[custom.models.OrderCustom],
):
    """Returns order custom detail for designers"""

    context_object_name = 'order'
    template_name = 'custom/custom_detail.html'
    model = custom.models.OrderCustom

    def get_queryset(self) -> QuerySet[Any]:
        """Returns queryset"""
        order_id = self.kwargs.get('pk')
        order_qs = custom.models.OrderCustom.objects.filter(
            is_published=True, pk=order_id
        )
        order = get_object_or_404(order_qs, pk=order_id)
        if not (order.designer is None) and (
            order.designer.id != self.request.user.id
        ):
            raise Http404()
        return order_qs

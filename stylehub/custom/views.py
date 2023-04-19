"""Views of custom app"""
from typing import Any

from django.contrib.auth import mixins
from django.db.models import QuerySet
from django.views import generic
from django.http import Http404

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
        return auth.models.User.designers.best_custom_evaluations()


class CustomDetail(
    mixins.PermissionRequiredMixin,
    generic.DetailView[custom.models.OrderCustom],
):
    """"""

    context_object_name = 'order'
    template_name = 'custom/custom_detail.html'
    model = custom.models.OrderCustom

    def get_queryset(self) -> QuerySet[Any]:
        print(self.request.user.is_designer)
        order = custom.models.OrderCustom.objects.get(pk=self.kwargs.get('pk'))
        if not (order.designer is None) and (
            order.designer.id != self.request.user.id
        ):
            raise Http404()
        return QuerySet(order)

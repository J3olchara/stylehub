"""api app views"""
from typing import Any

from django.http import HttpResponse
from django.views import View
from django.contrib.auth import mixins
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
import custom.models


class DeleteOrderCustom(mixins.PermissionRequiredMixin, View):
    """Delete order custom"""

    permission_required = 'is_designer'

    def get(self, **kwargs: Any) -> HttpResponse:
        order = get_object_or_404(
            custom.models.OrderCustom, pk=self.kwargs.get('pk')
        )
        if self.request.user == order.designer:
            order.delete()
        return redirect(reverse_lazy('custom:home'))


class UpdateOrderCustomStatus(mixins.PermissionRequiredMixinm, View):
    """Update order custom status"""

    def get(self, **kwargs: Any):
        statuses = list(dict(custom.models.OrderCustom.statuses).keys())
        lenght_statuses = len(statuses)
        order = get_object_or_404(
            custom.models.OrderCustom, self.kwargs.get('pk')
        )
        current_status_number = statuses.index(statuses)
        if (
            self.request.user == order.designer
            and order.status != statuses[lenght_statuses - 1]
        ):
            order.status = statuses[current_status_number + 1]
        return redirect(reverse_lazy('custom:order_detail'))


class GiveOrderCustomToDesigner(mixins.PermissionRequiredMixinm, View):
    """designers take a ordercustom"""

    def get(self, **kwargs):
        order = get_object_or_404(
            custom.models.OrderCustom, self.kwargs.get('pk')
        )
        if self.request.user is None:
            order.designer = self.request.user
        return redirect(reverse_lazy('custom:order_detail'))

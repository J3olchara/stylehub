"""api app views"""
from typing import Any

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

import auth.mixins
import custom.models


class DeleteOrderCustom(auth.mixins.DesignerRequiredMixin, View):
    """Delete order custom"""

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """
        funcion which mark irdercustom
        as unpublished and this order will not be displayed
        """
        order = get_object_or_404(
            custom.models.OrderCustom, pk=self.kwargs.get('pk')
        )
        if self.request.user == order.user:
            order.is_published = False
            order.save()
        return redirect(reverse_lazy('custom:home'))


class UpdateOrderCustomStatus(auth.mixins.DesignerRequiredMixin, View):
    """Update order custom status"""

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """funcion which update order with id from get request"""
        order_id = self.kwargs.get('pk')
        statuses = list(dict(custom.models.OrderCustom.statuses).keys())
        lenght_statuses = len(statuses)
        order = get_object_or_404(custom.models.OrderCustom, pk=order_id)
        current_status_number = statuses.index(order.status)
        if (
            self.request.user == order.designer
            and order.status != statuses[lenght_statuses - 1]
        ):
            order.status = statuses[current_status_number + 1]
        order.save()
        return redirect(
            reverse_lazy('custom:order_detail', kwargs={'pk': order_id})
        )


class GiveOrderCustomToDesigner(auth.mixins.DesignerRequiredMixin, View):
    """designers take a ordercustom. allowed only for designers and staff"""

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        """
        funcion which set
        order.designer = request.user with id from get request
        """
        order = get_object_or_404(
            custom.models.OrderCustom, pk=self.kwargs.get('pk')
        )
        order_id = self.kwargs.get('pk')
        if order.designer is None:
            order.designer = self.request.user
            order.save()
            return redirect(
                reverse_lazy('custom:order_detail', kwargs={'pk': order_id})
            )
        raise Http404

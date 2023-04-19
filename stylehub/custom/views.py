"""Views of custom app"""
from typing import Any

from django.contrib.auth import mixins
from django.db.models import QuerySet
from django.views import generic

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

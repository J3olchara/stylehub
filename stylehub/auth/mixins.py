"""auth mixins"""
from typing import Any

from django.contrib.auth.mixins import AccessMixin
from django.http import Http404, HttpRequest


class DesignerRequiredMixin(AccessMixin):
    """Verify that the current user is designer."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """checks user permissions to access designer only page"""
        if request.user.is_authenticated and (
            request.user.is_designer or request.user.is_staff
        ):
            return super().dispatch(request, *args, **kwargs)
        raise Http404()

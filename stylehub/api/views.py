"""APP api views"""
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

import clothes.models


class ToggleLiked(View):
    """toggle item from user`s liked"""

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """toggle item from user`s 'liked'"""
        item = clothes.models.Item.objects.get(id=kwargs.get('item_id'))
        user = request.user
        if item not in user.saved.all():
            user.saved.add(item)
        else:
            user.saved.remove(item)
        user.save()
        return HttpResponse("ok")

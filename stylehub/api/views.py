from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import RedirectView

import clothes.models


class ToggleLiked(RedirectView):
    """toggle item from user`s liked"""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        print(request.query_params)
        # item = clothes.models.Item.objects.get()
        return HttpResponse("ok")

"""
Context processor
creates some variables for all templates
"""
from typing import Any, Dict

from django.http import HttpRequest

import auth.models


def user_items_processor(request: HttpRequest) -> Dict[str, Any]:
    """returns items, user liked"""
    if not request.user.is_authenticated:
        return {}

    user_id = request.user.id
    return {
        'user_liked_items': auth.models.User.objects.get(
            id=user_id
        ).saved.all()
    }

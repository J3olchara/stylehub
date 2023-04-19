"""utils for market"""
from typing import Any

from django.conf import settings


def get_order_picture_dir(**kwargs: Any) -> str:
    """returns order_picture dir"""
    return f'{settings.UPLOAD_DIR}/order_pictures/'

"""utils for market app"""
from typing import Any
from uuid import uuid4

from django.conf import settings

path_mapping = {
    'Item': 'uploads/items/main_images',
    'ItemPicture': 'uploads/items/items_gallery',
}


def get_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from
    some model file field

    all paths that mapping files is in path_mapping
    'ModelClassName': 'path/from/media'
    """
    global path_mapping
    try:
        path = path_mapping[instance.__class__.__name__]
    except KeyError:
        path = 'Unknown'
    name = str(uuid4()) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_ROOT / path / name)

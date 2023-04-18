"""functions which are using in all project"""
from typing import Any
from uuid import uuid4

from django.conf import settings


def get_item_images_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    path = 'uploads/items'
    designer = str(instance.item.designer.id)
    name = str(instance.item.id) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_URL / path / designer / name)


def get_item_main_image_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from item model(image)
    """
    'Detected path traversal attempt in'
    path = 'uploads/items'
    if hasattr(instance, 'designer'):
        designer = str(instance.designer.id)
    else:
        designer = str(instance.item.designer.id)
    name = 'image' + str(instance.id) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_URL / path / designer / name)


def get_message_image_upload_location(filename: str, **kwargs: Any) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    path = 'uploads/chat/messages'
    name = f'{uuid4()}.{filename.split(".")[-1]}'
    return str(settings.MEDIA_URL / path / name)

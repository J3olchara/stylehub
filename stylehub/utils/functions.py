"""functions which are using in all project"""
from typing import Any
from uuid import uuid4

from django.conf import settings


def get_item_images_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    path = 'uploads/items'
    designer = str(instance.item.designer__id)
    name = str(uuid4()) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_ROOT / path / designer / name)


def get_item_main_image_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from item model(main_image)
    """
    path = 'uploads/items'
    designer = str(instance.designer__id)
    name = 'main_image' + str(uuid4) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_ROOT / path / designer / name)


def get_message_image_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    path = 'uploads/chat/messages'
    name = f'{uuid4()}.{filename.split(".")[-1]}'
    return str(settings.MEDIA_ROOT / path / name)

"""functions which are using in all project"""
from typing import Any, Dict
from uuid import uuid4

from django.conf import settings


def get_file_location(**kwargs: Any) -> Dict[str, str]:
    """returns actual file locations"""
    return {
        'Collection': f'{settings.UPLOAD_DIR}/collections/%s/%s/',
        'Item': f'{settings.UPLOAD_DIR}/collections/%s/%s/',
        'ItemPicture': f'{settings.UPLOAD_DIR}/collections/%s/%s/',
        'Message': f'{settings.UPLOAD_DIR}/chat/messages',
    }


def get_image_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    model_name: Any = type(instance).__name__
    path = get_file_location()[model_name]
    if model_name == 'Collection':
        designer_id = instance.designer.id
        collection_id = instance.id
    elif model_name == 'Item':
        designer_id = instance.designer.id
        collection_id = instance.collection.id
    elif model_name == 'ItemPicture':
        designer_id = instance.item.designer.id
        collection_id = instance.item.collection.id
    else:
        return path
    path = path % (designer_id, collection_id)
    file_type = filename.split('.')[-1]
    name = f'{uuid4()}.{file_type}'
    return str(path + name)


def get_message_image_upload_location(
    instance: Any, filename: str, **kwargs: Any
) -> str:
    """
    Returns directory to upload file from ItemPicture(image)
    """
    path = get_file_location()[instance.__class__]
    file_type = filename.split('.')[-1]
    name = f'{uuid4()}.{file_type}'
    return str(path + name)

"""templatetags files for clothes app"""
from typing import Any, Collection, List, Optional, Union

from django import template
from django.db.models import Avg
from sorl.thumbnail import get_thumbnail

import auth.models
import core.models

register = template.Library()


@register.simple_tag()
def get_image_px(
    image: core.models.MainImageMixin,
    px: str,
    crop: str,
    quality: int,
) -> str:
    """returns image thumbnail"""
    return str(image.get_image_px(px=px, crop=crop, quality=quality).url)


@register.filter()
def get_avg_evaluation(user: auth.models.User) -> int:
    """get avg evaluation"""
    avg = user.evaluations.aggregate(avg_evaluations=Avg('value'))[
        'avg_evaluations'
    ]
    if avg is not None:
        return avg
    return 0


@register.simple_tag()
def comma_separated_styles(styles: List[str]) -> str:
    """get comma separated style names"""
    return ', '.join(map(lambda x: x.name, styles))


@register.filter()
def get_words_slice(value: str, words_count: str) -> str:
    """get word slices"""
    words = value.split(maxsplit=int(words_count))
    return ' '.join(words[:-1])


@register.simple_tag()
def get_image_px_by_url(
    image: str, px: str, crop: str, quality: int
) -> Optional[str]:
    """get image thumbnail by url"""
    if image:
        return str(get_thumbnail(image, px, crop=crop, quality=quality).url)
    return 'NaN'


@register.simple_tag()
def count(iterable_or_int: Union[Collection[Any], int]) -> List[int]:
    """returns count of iterable"""
    if isinstance(iterable_or_int, Collection):
        iterable_or_int = len(iterable_or_int)
    return list(range(iterable_or_int))

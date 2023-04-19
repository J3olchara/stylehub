from typing import Any, Collection, Iterable, List, Optional, Union

from django import template
from django.db.models import Avg
from sorl.thumbnail import get_thumbnail

import core.models

register = template.Library()


@register.simple_tag()
def get_image_px(
    image: core.models.MainImageMixin,
    px: str,
    crop: str,
    quality: int,
) -> str:
    return str(image.get_image_px(px=px, crop=crop, quality=quality).url)


@register.filter()
def get_avg_evaluation(user):
    avg = user.evaluations.aggregate(avg_evaluations=Avg('value'))[
        'avg_evaluations'
    ]
    if avg is not None:
        return avg
    return 0


@register.filter()
def get_worth_evaluation(user):
    if user.evaluations.count():
        return user.evaluations.last()
    return 0


@register.filter()
def get_best_evaluation(value, **kwargs):
    if value.evaluations.count():
        return value.evaluations.first()
    return 0


@register.simple_tag()
def comma_separated_styles(styles: List[str]) -> str:
    return ', '.join(map(lambda x: x.name, styles))


@register.filter()
def get_words_slice(value: str, words_count: str) -> str:
    words = value.split(maxsplit=int(words_count))
    return ' '.join(words[:-1])


@register.simple_tag()
def get_image_px_by_url(
    image: str, px: str, crop: str, quality: int
) -> Optional[str]:
    if image:
        return str(get_thumbnail(image, px, crop=crop, quality=quality).url)
    return 'NaN'


@register.simple_tag()
def count(iterable_or_int: Union[Collection[Any], int]) -> List[int]:
    if isinstance(iterable_or_int, Collection):
        iterable_or_int = len(iterable_or_int)
    return list(range(iterable_or_int))

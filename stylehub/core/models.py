"""CORE abstract models"""
from datetime import datetime
from typing import Any, Union

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from django.utils.safestring import SafeString
from sorl.thumbnail import get_thumbnail

import core.utils
import utils.functions


class CreatedEdited(models.Model):
    """
    Model for models that uses creation date and editing date

    created: datetime. creation datetime
    edited: datetime. editing datetime
    """

    created: Union[datetime, Any] = models.DateTimeField(
        verbose_name='дата и время создания',
        help_text='Когда объект был создан',
        auto_now_add=True,
    )
    edited: Union[datetime, Any] = models.DateTimeField(
        verbose_name='дата и время редактирования',
        help_text='Когда объект в последний раз редактировали',
        auto_now=True,
    )

    class Meta:
        """settings for creatededited model"""

        abstract = True


class BaseCreature(CreatedEdited):
    """
    BaseCreature model for models like category, tag< style and other

    name: char[50]. Creature name.
    slug: char[50]. creature normalized name.
    created: datetime. Creation datetime.
    edited: datetime. Editing datetime.
    """

    name: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
        verbose_name='название',
        help_text='Придумайте название',
        max_length=50,
        blank=False,
        null=False,
    )
    slug: Union[str, 'models.SlugField[Any, Any]'] = models.SlugField(
        verbose_name='слаг',
        help_text='Нормализованное имя',
        unique=True,
    )

    def clean(self) -> None:
        self.slug = self.get_slug()
        if type(self).objects.filter(slug=self.slug).exists():
            raise ValidationError('Объект с таким именем уже существует')
        self.name = self.name.capitalize()
        return super().clean()

    def get_slug(self) -> str:
        """
        creates slug by translating object username
        :return: normalized name
        """
        slug: str = self.name.upper()
        translate_tab = str.maketrans(core.utils.normalize_table)
        return slug.translate(translate_tab).lower()

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'

    class Meta:
        """Model settings"""

        abstract = True


class MainImageMixin(models.Model):
    """
    MainPhoto Model for Item
    image: second-needed image for gallery
    """

    image: 'models.ImageField' = models.ImageField(
        verbose_name='обложка',
        help_text='Загрузите фото',
        upload_to=utils.functions.get_image_upload_location,
        max_length=255,
        null=True,
    )

    def get_image_px(
        self, px: str = '300x400', crop: str = 'center', quality: int = 70
    ) -> Any:
        """
        crops the picture
        px: string. format of the new image (1200x400, 1200)
        crop: string. crop centering
        quality: integer. quality of the new image
        """
        return get_thumbnail(self.image, px, crop=crop, quality=quality)

    def crop_item_img(self) -> Any:
        """
        crops the picture for item card
        """
        return self.get_image_px(px='325x150', quality=100)

    def get_image_1500_400(self) -> Any:
        """
        crops the picture
        px: string. format of the new image (1200x400, 1200)
        crop: string. crop centering
        quality: integer. quality of the new image
        """
        return self.get_image_px(px='1500x400', quality=100)

    def image_tmb(self) -> Union[SafeString, Any]:
        """returns HTML picture for Item"""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50">')
        return mark_safe('Изображения нет')

    @property
    def get_url(self) -> str:
        """returns url like 'uploads/...'"""
        return self.image.url

    def __str__(self) -> str:
        return str(self.image.url)

    class Meta:
        """for meta information"""

        abstract = True

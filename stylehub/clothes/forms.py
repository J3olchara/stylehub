"""
clothes forms
"""
from typing import Any, List, Optional, Tuple

from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

import auth.models
import clothes.models
import market.models


def get_choices(
    queryset: QuerySet[Any], field1: str, field2: str
) -> List[Tuple[Any, Any]]:
    """returns list of choices from queryset"""
    choices = []
    for obj in queryset.iterator():
        choices.append((obj.__dict__[field1], obj.__dict__[field2]))
    return choices


class BaseDesignerForm(forms.ModelForm[Any]):
    """abstract designer form that have initial designer=request.user"""

    def __init__(
        self,
        *args: Any,
        designer: Optional[auth.models.User] = None,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        designer_field = self.fields.get('designer')
        designer_field.widget = forms.widgets.HiddenInput()
        if designer is not None:
            designer_field.initial = designer


class CollectionCreateForm(BaseDesignerForm):
    """form that creates a new collection"""

    class Meta:
        """form settings"""

        model = clothes.models.Collection
        fields = [
            model.name.field.name,
            model.image.field.name,
            model.styles.field.name,
            model.text.field.name,
            model.designer.field.name,
        ]
        widgets = {
            model.name.field.name: forms.widgets.TextInput(
                attrs={'class': 'form-control'}
            ),
            model.image.field.name: forms.widgets.FileInput(
                attrs={'class': 'form-control'}
            ),
            model.styles.field.name: forms.widgets.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            model.text.field.name: forms.widgets.Textarea(
                attrs={'class': 'form-control'}
            ),
            model.designer.field.name: forms.widgets.Select(
                attrs={'class': 'form-control'}
            ),
        }


class ItemCreateForm(BaseDesignerForm):
    """form that creates a new collection"""

    def __init__(
        self,
        *args: Any,
        designer: Optional[auth.models.User] = None,
        **kwargs: Any
    ):
        super().__init__(*args, designer=designer, **kwargs)
        gallery_field = self.fields.get('gallery')
        category_field = self.fields.get('category')
        collection_field = self.fields.get('collection')

        gallery_field.label = _('Галерея')
        gallery_field.help_text = _('Приложите допольнительные фото')

        category_field.choices = get_choices(
            market.models.CategoryExtended.objects.all(), 'id', 'name'
        )

        collection_field.choices = get_choices(
            clothes.models.Collection.objects.filter(designer=designer),
            'id',
            'name',
        )

    gallery = forms.FileField(
        label='Приложенные файлы',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            }
        ),
    )

    def save(
        self, commit: bool = True, files: Optional[List[UploadedFile]] = None
    ) -> Any:
        """custom save method to create ItemPicture objects for item gallery"""
        item = super().save(commit)
        if files:
            clothes.models.ItemPicture.objects.create_many(
                images=files, item=item
            )
        return item

    class Meta:
        """form settings"""

        model = clothes.models.Item
        fields = [
            model.name.field.name,
            model.image.field.name,
            'gallery',
            model.cost.field.name,
            model.category.field.name,
            model.collection.field.name,
            model.styles.field.name,
            model.gender.field.name,
            model.text.field.name,
            model.designer.field.name,
        ]
        widgets = {
            model.name.field.name: forms.widgets.TextInput(
                attrs={'class': 'form-control'}
            ),
            model.image.field.name: forms.widgets.FileInput(
                attrs={'class': 'form-control'}
            ),
            model.cost.field.name: forms.widgets.NumberInput(
                attrs={'class': 'form-control'}
            ),
            model.category.field.name: forms.widgets.Select(
                attrs={'class': 'form-control'},
            ),
            model.collection.field.name: forms.widgets.Select(
                attrs={'class': 'form-control'},
            ),
            model.styles.field.name: forms.widgets.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            model.gender.field.name: forms.widgets.Select(
                attrs={'class': 'form-control'},
            ),
            model.text.field.name: forms.widgets.Textarea(
                attrs={'class': 'form-control'}
            ),
            model.designer.field.name: forms.widgets.Select(
                attrs={'class': 'form-control'}
            ),
        }

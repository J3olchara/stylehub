"""
forms for custom app

write your forms here
"""
from typing import Any, Optional

from django import forms
from django.utils.translation import gettext_lazy as _

import auth.models
import custom.models

# from pinscrap.pinterest import PinterestImageScraper


class OrderCustomStartCreateForm(forms.ModelForm[custom.models.OrderCustom]):
    """form for creating pinterest custom order"""

    pins = forms.ChoiceField(
        label=_('Выбранные фото с пинтереста'),
        choices=[],
        widget=forms.HiddenInput(),
    )

    def __init__(
        self,
        *args: Any,
        user: Optional[auth.models.User] = None,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        user_field = self.fields.get('user')

        user_field.widget = forms.widgets.HiddenInput()
        if user is not None:
            user_field.initial = user

    # def get_choices(self):
    #     if self.cleaned_data['header']:
    #         pinterest = PinterestImageScraper()
    #         urls = pinterest.get_image_urls(key=self.cleaned_data['header'])
    #         print(urls)

    class Meta:
        """settings for OrderCustomForm"""

        model = custom.models.OrderCustom

        fields = [
            model.user.field.name,
            model.header.field.name,
            model.max_price.field.name,
            model.text.field.name,
        ]

        widgets = {
            model.header.field.name: forms.widgets.TextInput(
                attrs={'class': 'form-control'}
            ),
            model.max_price.field.name: forms.widgets.NumberInput(
                attrs={'class': 'form-control'}
            ),
            model.text.field.name: forms.widgets.Textarea(
                attrs={'class': 'form-control'}
            ),
        }

""" Forms witch related to users/designer (auth app) """
from typing import Any, Dict, Union

from django import forms

from auth.models import DesignerProfile, User


class UserForm(forms.ModelForm[User]):
    """Form for change user info"""

    def __init__(
        self, *args: Any, readonly: bool = False, **kwargs: Any
    ) -> None:
        """Init to break opportunity user edit random profile"""
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['readonly'] = readonly

    class Meta:
        """Meta class for modelform"""

        model = User

        fields = ('gender', 'email', 'username', 'first_name', 'last_name')

        labels = {
            'gender': 'Пол',
            'email': 'Электронная почта',
            'username': 'никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

        widgets = {
            'gender': forms.RadioSelect(),
            'email': forms.EmailInput(),
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }


class DesignerProfileForm(forms.ModelForm[DesignerProfile]):
    """Form for change Designer profile"""

    def __init__(
        self, *args: Any, readonly: bool = False, **kwargs: Any
    ) -> None:
        """Init to break opportunity user edit random profile"""
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['readonly'] = readonly

    class Meta:
        """Meta class for modelform"""

        model = DesignerProfile

        fields = ('avatar', 'background', 'text')

        labels = {
            'avatar': 'Аватар дизайнера',
            'background': 'Задний фон',
            'text': 'Информация о дизайнере',
        }

        widgets = {'text': forms.Textarea()}

    def save(
        self, commit: bool = False, files: Union[None, Dict[str, Any]] = None
    ) -> Any:
        """Rewrite save to save images"""
        instance = super().save(commit=commit)
        if not files:
            files = {}
        if 'avatar' in files.keys():
            instance.avatar = files['avatar']
        if 'background' in files.keys():
            instance.background = files['background']
        instance.save()

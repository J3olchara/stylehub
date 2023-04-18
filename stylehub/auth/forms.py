""" Forms witch related to users/designer (auth app) """
from typing import Any, Dict, Union, Optional

import django.contrib.auth.forms as default_forms
import django.contrib.auth.models as default_models
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import auth.models


class UserForm(forms.ModelForm[auth.models.User]):
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

        model = auth.models.User

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


class DesignerProfileForm(forms.ModelForm[auth.models.DesignerProfile]):
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

        model = auth.models.DesignerProfile

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


class LoginForm(default_forms.AuthenticationForm):
    """
    Login form to Login page

    username: str.
    password: str.
    remember_me: bool. Remember user.
    """

    remember_me = forms.BooleanField(
        label=_('Запомнить меня'),
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mb-4',
            }
        ),
        required=False,
    )

    def __init__(self, *args: Any, **kwargs: Any):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'placeholder': _('Username'),
            }
        )
        self.fields['password'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Password'),
                'type': 'password',
            }
        )


class PasswordChangeForm(default_forms.PasswordChangeForm):
    """
    Password reset form

    old_password: str.
    new_password1: str.
    new_password2: str. Need to be equal to new_password1.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'password',
            }
        )
        self.fields['old_password'].widget = widget
        self.fields['new_password1'].widget = widget
        self.fields['new_password2'].widget = widget


class PasswordResetForm(default_forms.PasswordResetForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'email',
            }
        )


class PasswordResetConfirmForm(default_forms.SetPasswordForm):
    """
    Password reset form. Allows user change his password if he forgot it.

    new_password1: str.
    new_password2: str. Need to be equal to new_password1.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'password',
            }
        )
        self.fields['new_password1'].widget = widget
        self.fields['new_password2'].widget = widget


class SignUpForm(default_forms.UserCreationForm):  # type: ignore[type-arg]
    """
    Sign up form. Create new users.

    username: str. Unique
    email: str. bicycle unique
    new_password1: str.
    new_password2: str. Need to be equal to new_password1.
    """

    email = forms.EmailField(
        label=_('Ваш email'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
            }
        ),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit: bool = True) -> auth.models.ActivationToken:
        """set extra fields to user."""
        instance = super(SignUpForm, self).save(commit=commit)
        instance.is_active = settings.NEW_USERS_ACTIVATED
        token = auth.models.ActivationToken.objects.create(
            user=instance,
        )
        instance.save()
        return token

    class Meta:
        model = auth.models.User
        fields = [
            model.email.field.name,
            model.username.field.name,
            f'{model.password.field.name}1',
            f'{model.password.field.name}2',
        ]

"""
auth views

views to user login/user create/user activate
"""
from typing import Any, Dict

import django.contrib.auth.views as default_views
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

import auth.forms
import auth.models


class CustomLoginView(default_views.LoginView):
    """
    Custom login page view
    Returns user auth form
    """

    form_class = auth.forms.LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form: Any) -> HttpResponse:
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class CustomChangePasswordDone(default_views.PasswordChangeDoneView):
    """
    Custom password change form
    Returns form that allows user change his password
    """

    template_name = 'auth/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['alerts'] = [
            {'type': 'success', 'text': _('Пароль успешно изменён')}
        ]
        return context


class CustomPasswordResetDone(default_views.PasswordResetDoneView):
    """
    Custom password reset page view
    Send reset email notigication
    """

    template_name = 'auth/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        head = _('Письмо с инструкциями по восстановлению пароля отправлено')
        p1 = _(
            'Мы отправили вам инструкцию по установке нового '
            'пароля на указанный адрес электронной почты'
            '(если в нашей базе данных есть такой адрес). '
            'Вы должны получить ее в ближайшее время.'
        )
        p2 = _(
            'Если вы не получили письмо, пожалуйста, убедитесь, что '
            'вы ввели адрес с которым Вы зарегистрировались,'
            ' и проверьте папку со спамом.'
        )
        context['message'] = (
            f'<h1>{head}</h1>\n' f'<p>{p1}</p>\n' f'<p>{p2}</p>'
        )
        return context


class CustomPasswordResetComplete(default_views.PasswordResetCompleteView):
    """
    Custom password reset page view
    Allows user change his password from received reset url.
    """

    template_name = 'auth/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['alerts'] = [
            {'type': 'success', 'text': _('Пароль успешно изменён')}
        ]
        return context


class SignUp(generic.FormView[auth.forms.SignUpForm]):
    """
    Returns signup form
    Allows guest sign up on the site
    """

    template_name = 'auth/signup.html'
    form_class = auth.forms.SignUpForm
    success_url = reverse_lazy('auth:signup_done')

    def form_valid(self, form: Any) -> HttpResponse:
        """when form is valid"""
        token = form.save()
        url = token.get_url(f'http://{get_current_site(self.request)}')
        username = form.data['username']
        message = (
            _(
                f'Благодарим за регистрацию на нашем сайте!\n\n'
                f'Ваш логин: {username}\n'
                f'Для активации аккаунта перейдите по ссылке\n'
            )
            + url
        )
        mail.send_mail(
            subject=str(_('Активация аккаунта')),
            message=message,
            from_email=settings.SITE_EMAIL,
            recipient_list=[form.data['email']],
        )
        return super().form_valid(form)


class SignUpDone(generic.TemplateView):
    """Sends confirmation url address"""

    template_name = 'auth/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['alerts'] = [
            {
                'type': 'success',
                'text': _(
                    'На вашу электронную отправлена ссылка '
                    'на активацию аккаунта.'
                ),
            }
        ]
        return context


class SignUpConfirm(generic.TemplateView):
    """
    Account activation page.
    Allows user to activate his new account.
    """

    template_name = 'auth/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user_id = int(self.kwargs.get('user_id'))
        token = self.kwargs.get('token')
        context = super().get_context_data(**kwargs)
        token = get_object_or_404(
            auth.models.ActivationToken.objects,
            user=user_id,
            token=token,
        )
        if not token.expired():
            token.user.is_active = True
            token.user.save()
            token.delete()
            context['alerts'] = [
                {
                    'type': 'success',
                    'text': _('Ваш аккаунт успешно активирован!'),
                }
            ]
        else:
            context['alerts'] = [
                {
                    'type': 'danger',
                    'text': _(
                        'Ссылка на активацию аккаунта истекла. '
                        'Обратитесь к администрации'
                    ),
                }
            ]
        return context

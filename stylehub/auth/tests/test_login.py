"""login tests for user auth"""
from django.urls import reverse
from django.conf import settings

import auth.tests.base
import auth.models


class LoginTests(auth.tests.base.AuthSetup):
    def test_login_by_username(self):
        path = reverse('auth:login')
        data = {'username': self.user.username, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertRedirects(
            response,
            settings.LOGIN_REDIRECT_URL,
            msg_prefix='Пользователь не может авторизоваться с логином'
        )

    def test_login_by_email(self):
        path = reverse('auth:login')
        data = {'username': self.user.email, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertRedirects(
            response,
            settings.LOGIN_REDIRECT_URL,
            msg_prefix='Пользователь не может авторизоваться с почтой'
        )

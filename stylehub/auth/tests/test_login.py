"""login tests for user auth"""
from django.conf import settings
from django.urls import reverse

import auth.models
import auth.tests.base


class LoginTests(auth.tests.base.AuthSetup):
    """tests to user authenticate"""

    def test_login_by_username(self):
        """tests that user can login by username"""
        path = reverse('auth:login')
        data = {'username': self.user.username, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertRedirects(
            response,
            settings.LOGIN_REDIRECT_URL,
            msg_prefix='Пользователь не может авторизоваться с логином',
        )

    def test_login_by_email(self):
        """tests that user can login by email"""
        path = reverse('auth:login')
        data = {'username': self.user.email, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertRedirects(
            response,
            settings.LOGIN_REDIRECT_URL,
            msg_prefix='Пользователь не может авторизоваться с почтой',
        )

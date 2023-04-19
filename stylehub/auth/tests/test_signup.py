"""
testing user signup
"""
from datetime import timedelta

import mock
from django.test import Client, override_settings
from django.urls import reverse

import auth.forms
import auth.models
import auth.tests.base


class SignUpTests(auth.tests.base.AuthSetup):
    """tests signup features"""

    @staticmethod
    def get_inactive_user_and_token():
        """returns inactive user and his activation token"""
        user = auth.models.User.inactive.create_user(
            username='fsfgsegfesefefssefef',
            email='3efesafesa@gmail.com',
            password='142kjjkgrsgeew3gesrg',
        )
        token = auth.models.ActivationToken.objects.create(user=user)
        return user, token

    @override_settings(NEW_USER_IS_ACTIVE=False)
    @mock.patch('auth.models.datetime')
    def test_activation_false(self, mocked_datetime):
        """tests that expired token cant be used"""
        user, token = self.get_inactive_user_and_token()
        path = reverse(
            'auth:signup_confirm',
            kwargs={'token': token.token, 'user_id': user.id},
        )
        mocked_datetime.now.return_value = token.expire + timedelta(minutes=1)
        resp = Client().get(path)
        user = auth.models.User.objects.get(id=user.id)
        self.assertIn(
            'alerts',
            resp.context,
            msg='Пользователь не получает ошибок активации',
        )
        self.assertEqual(
            'danger',
            resp.context['alerts'][0]['type'],
            msg='Пользователь не получает красных ошибок активации',
        )
        self.assertTrue(
            not user.is_active,
            msg=(
                'Пользователь активируется, '
                'независимо от переменной NEW_USER_IS_ACTIVE'
            ),
        )

    @mock.patch('auth.models.datetime')
    @override_settings(NEW_USER_IS_ACTIVE=False)
    def test_activation_true(self, mocked_datetime):
        """tests that user can activate new account"""
        user, token = self.get_inactive_user_and_token()
        path = reverse(
            'auth:signup_confirm',
            kwargs={'token': token.token, 'user_id': user.id},
        )
        mocked_datetime.now.return_value = token.expire - timedelta(minutes=1)
        resp = Client().get(path)
        user = auth.models.User.objects.get(id=user.id)
        self.assertIn(
            'alerts',
            resp.context,
            'Пользователь не получает уведомления об успешной активации',
        )
        self.assertEqual(
            'success',
            resp.context['alerts'][0]['type'],
            'Пользователь не получает зеленые уведомления',
        )
        self.assertTrue(
            user.is_active,
            msg=(
                'Пользователь активируется, '
                'независимо от переменной NEW_USER_IS_ACTIVE'
            ),
        )

    def test_env_activation_users(self):
        """tests variable that changes is_active for new users"""
        path = reverse('auth:signup')
        client = Client()
        with override_settings(NEW_USER_IS_ACTIVE=False):
            client.post(
                path,
                data={
                    'username': 'fake_username',
                    'password1': 'fake_password',
                    'password2': 'fake_password',
                    'email': 'email@yandex.ru',
                },
            )
            user = auth.models.User.inactive.get(username='fake_username')
            self.assertTrue(not user.is_active)
        with override_settings(NEW_USER_IS_ACTIVE=True):
            resp = client.post(
                path,
                data={
                    'username': 'fake_username1',
                    'password1': 'fake_password1',
                    'password2': 'fake_password1',
                    'email': 'love_danila_eremin@seniorgoogle.com',
                },
            )
            self.assertRedirects(resp, reverse('auth:signup_done'))
            user = auth.models.User.objects.get(username='fake_username1')
            self.assertTrue(user.is_active)

from datetime import timedelta

from django.urls import reverse
from django.test import Client
import mock

import auth.tests.base
import auth.models
import auth.forms


class SignUpTests(auth.tests.base.AuthSetup):

    @mock.patch('authorisation.auth.models.datetime')
    def test_activation_false(self, mocked_datetime):
        path = reverse(
            'authorisation:signup_confirm',
            kwargs={'token': self.token.token, 'user_id': self.user.id},
        )
        mocked_datetime.now.return_value = self.token.expire + timedelta(
            minutes=1
        )
        resp = Client().get(path)
        self.user = auth.models.User.inactive.get(id=self.user.id)
        self.assertIn('alerts', resp.context)
        self.assertEqual(
            'danger',
            resp.context['alerts'][0]['type'],
            resp.context['alerts'][0]['text'],
        )
        self.assertTrue(not self.user.is_active, self.user.is_active)

    @mock.patch('authorisation.auth.models.datetime')
    def test_activation_true(self, mocked_datetime):
        path = reverse(
            'authorisation:signup_confirm',
            kwargs={'token': self.token.token, 'user_id': self.user.id},
        )
        mocked_datetime.now.return_value = self.token.expire - timedelta(
            minutes=1
        )
        resp = Client().get(path)
        self.user = auth.models.User.objects.get(id=self.user.id)
        self.assertIn('alerts', resp.context)
        self.assertEqual(
            'success',
            resp.context['alerts'][0]['type'],
            resp.context['alerts'][0]['text'],
        )
        self.assertTrue(self.user.is_active)

    # def test_env_activation_users(self):
    #     path = reverse('authorisation:signup')
    #     client = Client()
    #     with override_settings(NEW_USERS_ACTIVATED=False):
    #         client.post(
    #             path,
    #             data={
    #                 'username': 'fake_username',
    #                 'password1': 'fake_password',
    #                 'password2': 'fake_password',
    #                 'email': 'email@yandex.ru',
    #             },
    #         )
    #         user = auth.models.User.inactive.get(username='fake_username')
    #         self.assertTrue(not user.is_active)
    #     with override_settings(NEW_USERS_ACTIVATED=True):
    #         resp = client.post(
    #             path,
    #             data={
    #                 'username': 'fake_username1',
    #                 'password1': 'fake_password1',
    #                 'password2': 'fake_password1',
    #                 'email': 'love_danila_eremin@seniorgoogle.com',
    #             },
    #         )
    #         self.assertRedirects(resp, reverse('authorisation:signup_done'))
    #         user = auth.models.User.objects.get(username='fake_username1')
    #         self.assertTrue(user.is_active)

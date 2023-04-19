from django.urls import reverse

import auth.tests.base


class LoginTests(auth.tests.base.AuthSetup):
    def test_login_by_username(self):
        path = reverse('auth:login')
        data = {'username': self.user.username, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 302)

    def test_login_by_email(self):
        path = reverse('auth:login')
        data = {'username': self.user.email, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 302)

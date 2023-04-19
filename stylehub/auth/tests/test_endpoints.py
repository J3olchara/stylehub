"""
testing auth endpoints
"""
from django.test import TestCase
from django.urls import reverse


class TestEndpoints(TestCase):
    def test_signup_endpoint(self):
        path = reverse('auth:signup')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_signup_done_endpoint(self):
        path = reverse('auth:signup_done')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_login_endpoint(self):
        path = reverse('auth:login')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

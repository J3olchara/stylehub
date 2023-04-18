"""
testing auth endpoints
"""
from django.test import TestCase
from django.urls import reverse


class TestEndpoints(TestCase):
    def test_signup_endpoint(self):
        path = reverse('authorisation:signup')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_signup_done_endpoint(self):
        path = reverse('authorisation:signup_done')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_login_endpoint(self):
        path = reverse('authorisation:login')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

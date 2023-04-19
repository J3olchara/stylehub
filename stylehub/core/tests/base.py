"""
base classes for testing apps
"""
from django.urls import reverse
from django.test import TestCase

import auth.models


class EndpointTests(TestCase):
    """have comfortable function to test endpoints"""

    def setUp(self) -> None:
        self.user_password = 'hgdqghfgh3123eghf'
        self.designer_password = 'fsfss32effesfsesfesf123213'

        self.user = auth.models.User.objects.create_user(
            username='fhvjsfs',
            email='fesjkhfkjhefsjhk@gmail.com',
            password=self.user_password,
        )

        self.designer_user = auth.models.User.objects.create_user(
            username='fesjkhnsfehkjfejkdesigner',
            email='fesffsefsedesigner@gmail.com',
            password=self.designer_password,
        )

        self.designer1 = self.designer_user.make_designer()

    def endpoint(self, template_name, **kwargs):
        """tests clothes:recommend page endpoint"""
        path = reverse(template_name, kwargs=kwargs)
        self.assertEqual(self.client.get(path).status_code, 200)

    def auth_endpoint(self, template_name, **kwargs):
        """tests any auth needed endpoints"""
        path = reverse(template_name, kwargs=kwargs)

        self.assertEqual(self.client.get(path).status_code, 302)

        self.client.login(
            username=self.user.username, password=self.user_password
        )
        self.assertEqual(self.client.get(path).status_code, 200)

    def designer_endpoint(self, template_name, **kwargs):
        """tests endpoint that can view only designer"""
        path = reverse(template_name, kwargs=kwargs)

        self.assertEqual(self.client.get(path).status_code, 404)

        self.client.login(
            username=self.user.username, password=self.user_password
        )
        self.assertEqual(self.client.get(path).status_code, 404)

        self.client.login(
            username=self.designer_user.username,
            password=self.designer_password,
        )
        self.assertEqual(self.client.get(path).status_code, 200)

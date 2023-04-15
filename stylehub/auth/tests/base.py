"""base classes to auth tests"""
from django.test import TestCase

import auth.models


class AuthSetup(TestCase):
    """
    base test class for auth setup
    """

    def setUp(self) -> None:
        """auto vars for tests"""
        self.user = auth.models.User.objects.create_user(
            username='setup_test_username',
            email='setup_test_email@gmail.com',
            password='Verysecret',
        )

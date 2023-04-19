"""base classes to auth tests"""
from django.test import TestCase

import auth.models


class AuthSetup(TestCase):
    """
    base test class for auth setup
    """

    def setUp(self) -> None:
        """auto vars for tests"""
        self.user_password = 'fesfewsfaf324234fes'
        self.user = auth.models.User.active.create_user(
            username='fsfsfesefsfesfesfe',
            email='fsefsffesseffes@gmail.com',
            password=self.user_password,
        )

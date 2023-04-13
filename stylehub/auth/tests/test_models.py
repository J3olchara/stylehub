"""
Tests for auth models

write your model tests here
"""
from django.test import TestCase

import market.models
from auth.models import User


class TestUser(TestCase):
    """Tests for User model"""

    def setUp(self) -> None:
        """auto vars for tests"""
        self.user = User.objects.create_user(
            username='setup_test_username',
            email='setup_test_email@gmail.com',
            password='Verysecret',
        )

    def test_creating_cart(self):
        """tests that cart is creating when user creates"""
        test_username = 'ILOVEDANILAEREMIN'
        e_mail = 'google_danila@gmail.com'
        user = User.objects.create_user(username=test_username, email=e_mail)
        cart = market.models.Cart.objects.get(user=user)
        self.assertTrue(cart)
        test_username = 'ILOVEDANILAEREMIN1'
        e_mail = 'google_danila1@gmail.com'
        superuser = User.objects.create_superuser(
            username=test_username, email=e_mail
        )
        cart = market.models.Cart.objects.get(user=superuser)
        self.assertTrue(cart)

    def test_make_designer(self):
        """testing that user can to be designer"""
        designer_profile = self.user.make_designer()
        self.assertTrue(designer_profile)

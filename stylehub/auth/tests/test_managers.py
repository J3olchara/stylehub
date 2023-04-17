"""
tests for auth managers

write your function tests here
"""
from django.test import override_settings

import auth.models
import clothes.models
from auth.tests.base import AuthSetup
from market.tests.base import MarketSetUp


class TestDesigner(MarketSetUp, AuthSetup):
    """
    tests designer manager of User model
    """

    def test_get(self):
        """tests that user have become designer"""
        self.user.make_designer()
        designer = auth.models.User.designers.get(id=self.user.id)
        self.assertTrue(designer.is_designer)
        self.assertTrue(designer.designer_profile)

    def test_unpopular(self):
        """tests auth.models.User.designers.unpopular"""
        designer = auth.models.User.designers.create_user(
            username='fdsfdsfdsfds',
            email='danilaereminlove@gmail.com',
            password='1234fseffsedfRDewfefegsg21',
        )
        item = clothes.models.Item.objects.create(
            name='item_name1231',
            designer=designer,
            cost=99999,
            category=self.category_extended1,
            collection=self.collection1,
            bought=9,
        )
        with override_settings(POPULAR_DESIGNER_BUYS=10):
            auth.models.User.designers.unpopular().get(id=designer.id)
            item.bought = 10
            item.save()
            with self.assertRaises(auth.models.User.DoesNotExist):
                auth.models.User.designers.unpopular().get(id=designer.id)

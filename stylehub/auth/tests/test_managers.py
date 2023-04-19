"""
tests for auth managers

write your function tests here
"""
from django.test import TestCase, override_settings

import auth.models
import clothes.models
import custom.models
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


class TestDesignersManager(TestCase):
    """Test designers managers tests"""

    @override_settings(DESIGNERS_ON_CUSTOM_MAIN_PAGE=2)
    def test_best_designers_on_custom_evaluation(self):
        """test best_designers_on_custom_evaluation method"""
        self.tearDown()
        user_password = 'oipperwoperwopopretopkjgflcvm'
        designer_user_password_1 = 'tyrertewqtreretuiopi'
        designer_user_password_2 = 'fdfsdafdgkdfjmnvmncbmnc'
        user = auth.models.User.objects.create_user(
            username='test_user',
            email='testuser@gmail.com',
            password=user_password,
        )
        designer1 = auth.models.User.designers.create_user(
            username='designer_user',
            email='designer_user@gmail.com',
            password=designer_user_password_1,
        )
        designer2 = auth.models.User.designers.create_user(
            username='designer_user2',
            email='designer_user2@mail.com',
            password=designer_user_password_2,
        )

        order_custom = custom.models.OrderCustom.objects.create(
            user=user,
            designer=designer1,
            header='test',
            max_price=1232231,
            text='text',
        )
        custom.models.OrderCustomEvaluation.objects.create(
            user=user, order=order_custom, rating=4
        )

        designers = auth.models.User.designers.best_custom_evaluations()
        lenght = len(designers)
        self.assertEqual(designers[lenght - 1], designer2)
        with override_settings(DESIGNERS_ON_CUSTOM_MAIN_PAGE=1):
            new_designers = (
                auth.models.User.designers.best_custom_evaluations()
            )
            self.assertEqual(len(new_designers), 1)
            self.assertEqual(new_designers[0], designer1)

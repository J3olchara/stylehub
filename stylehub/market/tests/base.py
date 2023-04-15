"""base classes to market tests"""
from django.test import TestCase

import auth.models
import market.models


class MarketSetUp(TestCase):
    """
    base test class for market setup

    have all model objects from market models
    """

    def setUp(self) -> None:
        self.user_password = '1231313213dfsafdqw312'
        self.designer_password = '123456765sdffghhgjf123'
        self.user = auth.models.User.objects.create_user(
            username='some_so_uqi13231',
            email='desaofesijf@gmail.com',
            password=self.user_password,
        )
        self.designer_user = auth.models.User.objects.create_user(
            username='this_user_will_be_a_designer',
            email='designer@gmail.com',
            password=self.designer_password,
        )
        self.designer1 = self.designer_user.make_designer()
        self.style1 = market.models.Style.objects.create(name='some_style1')
        self.category_base1 = market.models.CategoryBase.objects.create(
            name='cat_base1'
        )
        self.category_extended1 = (
            market.models.CategoryExtended.objects.create(
                name='cat_extended1',
                category_base=self.category_base1,
            )
        )
        self.collection1 = market.models.Collection.objects.create(
            name='some_collection1', designer=self.user
        )
        self.item1 = market.models.Item.objects.create(
            name='item_name1231',
            designer=self.user,
            cost=99999,
            category=self.category_extended1,
            collection=self.collection1,
        )
        self.item1.styles.add(self.style1)
        self.item1.save()
        self.collection1.save()

""" test clothes app managers """

import clothes.models
from market.tests.base import MarketSetUp


class TestOrdersManager(MarketSetUp):
    """class for Test OrdersManager"""

    def test_get_user_orders(self):
        """test order manager test_get_user_orders method"""
        self.order = clothes.models.OrderClothes.objects.create(
            user=self.user,
            designer=self.designer_user,
            item=self.item1,
            sum=1200,
        )
        self.order1 = clothes.models.OrderClothes.objects.create(
            user=self.user,
            designer=self.designer_user,
            item=self.item2,
            sum=self.item2.cost,
        )
        orders = clothes.models.OrderClothes.objects.get_user_orders(self.user)
        self.assertEqual(len(orders), 2)

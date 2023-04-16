""" test clothes app managers """

import clothes.models
from market.tests.base import MarketSetUp


class TestOrdersManager(MarketSetUp):
    """class for Test OrdersManager"""

    def test_get_user_orders(self):
        """test order manager test_get_user_orders method"""
        orders = clothes.models.OrderClothes.objects.get_user_orders(self.user)
        self.assertEqual(len(orders), 2)

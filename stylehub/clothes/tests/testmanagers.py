""" test clothes app managers """

import auth.models
import clothes.models
from market.tests.base import MarketSetUp


class TestOrdersManager(MarketSetUp):
    """class for Test OrdersManager"""

    def test_get_user_orders(self):
        """test order manager test_get_user_orders method"""
        self.order_user_password = 'sghhgfdsdfsdfasdhgfdfsda'
        self.order_designer_user_password = 'rfghjfsdfsbvncxvcxzvcbnvnbvcvbx'

        self.order_user = auth.models.User.objects.create_user(
            username='test_order_cloth_user',
            email='test_order_cloth_user@gmail.com',
            password=self.order_user_password,
        )
        self.order_designer_user = auth.models.User.objects.create_user(
            username='test_order_cloth_designer_user',
            email='test_order_cloth_designer_user@gmail.com',
            password=self.order_designer_user_password,
        )
        self.order_designer = self.order_designer_user.make_designer()

        self.order = clothes.models.OrderClothes.objects.create(
            user=self.order_user,
            designer=self.order_designer_user,
            item=self.item1,
            sum=self.item1.cost,
        )
        self.order = clothes.models.OrderClothes.objects.create(
            user=self.order_user,
            designer=self.order_designer_user,
            item=self.item2,
            sum=self.item2.cost,
        )
        orders = clothes.models.OrderClothes.objects.get_user_orders(
            self.order_user
        )
        self.assertEqual(len(orders), 2)

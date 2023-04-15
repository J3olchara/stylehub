"""
tests for market models

write your own tests here
"""
from auth.tests.base import AuthSetup
from market.tests.base import MarketSetUp


class TestItem(MarketSetUp, AuthSetup):
    """tests Item model methods"""

    def test_buy(self):
        """tests item method buy"""
        past = self.item1.bought
        order = self.item1.buy(self.user)
        self.assertEqual(past + 1, self.item1.bought)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.sum, order.item.cost)

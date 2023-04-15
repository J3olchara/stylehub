"""
Tests for market model managers

write your model manager tests here
"""
import market.models
from market.tests.base import MarketSetUp


class TestItem(MarketSetUp):
    """tests item manager"""

    def test_item_details(self):
        """
        tests item_details function

        item must have prefetched evaluations
        """
        item = market.models.Item.objects.get_details().get(id=self.item1.id)
        self.assertIn('evaluations', item._prefetched_objects_cache.keys())

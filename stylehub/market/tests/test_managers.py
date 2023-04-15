"""
Market model managers tests

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


class TestCollectionManager(MarketSetUp):
    """test class for Collection manager functions"""

    def test_get_items_in_collection(self):
        """tests that get_items_in_collection queryset have prefetched items"""
        collection = (
            market.models.Collection.objects.get_items_in_collection().get(
                id=self.collection1.id
            )
        )
        self.assertIn('items', collection._prefetched_objects_cache.keys())

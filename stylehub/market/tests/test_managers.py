""" Test managers from market app"""

import market.models
import market.tests.base


class TestCollectionManager(market.tests.base.SetUpBaseClass):
    """test class for Collection manager functions"""

    def test_get_items_in_collection(self):
        """tests that get_items_in_collection queryset have prefetched items"""
        collection = (
            market.models.Collection.objects.get_items_in_collection().get(
                id=self.collection1.id
            )
        )
        self.assertIn('items', collection._prefetched_objects_cache.keys())

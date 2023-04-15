""" Test managers from market app"""

import market.models
import market.tests.base


class TestManagers(market.tests.base.SetUpBaseClass):
    """ Class for test managers """
    def test_collection_manager(self):
        """ Test collection manager function get_items_in_collection """
        collection = (
            market.models.Collection.objects.get_items_in_collection().get(
                id=self.collection1.id
            )
        )
        # print(collection._prefetched_objects_cache.keys())
        self.assertIn('items', collection._prefetched_objects_cache.keys())

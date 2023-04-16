"""
Market model managers tests

write your model manager tests here
"""
from django.test import override_settings

import clothes.models
from auth.tests.base import AuthSetup
from market.tests.base import MarketSetUp


class TestItem(MarketSetUp):
    """tests item manager"""

    def test_item_details(self):
        """
        tests item_details function

        item must have prefetched evaluations
        """
        item = clothes.models.Item.objects.get_details().get(id=self.item1.id)
        self.assertIn('evaluations', item._prefetched_objects_cache.keys())


class TestCollectionManager(MarketSetUp, AuthSetup):
    """test class for Collection manager functions"""

    def test_get_items_in_collection(self):
        """tests that get_items_in_collection queryset have prefetched items"""
        collection = (
            clothes.models.Collection.objects.get_items_in_collection().get(
                id=self.collection1.id
            )
        )
        self.assertIn('items', collection._prefetched_objects_cache.keys())

    def test_recommend(self):
        """
        tests that method returns popular
        collections with user last styles
        """
        self.user.last_styles.set(self.collection1.styles.all())
        self.user.save()
        with override_settings(POPULAR_COLLECTION_BUYS=10):
            collections = clothes.models.Collection.objects.recommend(
                self.user
            )
            self.assertNotIn(self.collection1, collections)

            self.item1.bought = 11
            self.item1.save()

            collections = clothes.models.Collection.objects.recommend(
                self.user
            )
            self.assertIn(self.collection1, collections)

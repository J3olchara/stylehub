"""
Market model managers tests

write your model manager tests here
"""
from django.test import override_settings

import auth.models
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
        collection = clothes.models.Collection.objects.with_items().get(
            id=self.collection1.id
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

    def test_unpopular(self):
        """tests auth.models.Item.unpopular"""
        designer = auth.models.User.designers.create_user(
            username='123u213h12j312h3h213',
            email='dsahadw312j3j213jhjf@gmail.com',
            password='12fwejfjkje12',
        )
        item = clothes.models.Item.objects.create(
            name='item_name1231',
            designer=designer,
            cost=99999,
            category=self.category_extended1,
            collection=self.collection1,
            bought=9,
        )
        with override_settings(POPULAR_DESIGNER_BUYS=10):
            self.assertIn(item, clothes.models.Item.objects.unpopular().all())

            item.bought = 10
            item.save()
            self.assertNotIn(
                item, clothes.models.Item.objects.unpopular().all()
            )

    def test_get_user_orders(self):
        """test order manager test_get_user_orders method"""
        order_user_password = 'sghhgfdsdfsdfasdhgfdfsda'
        order_designer_user_password = 'rfghjfsdfsbvncxvcxzvcbnvnbvcvbx'

        order_user = auth.models.User.objects.create_user(
            username='test_order_cloth_user',
            email='test_order_cloth_user@gmail.com',
            password=order_user_password,
        )
        order_designer_user = auth.models.User.objects.create_user(
            username='test_order_cloth_designer_user',
            email='test_order_cloth_designer_user@gmail.com',
            password=order_designer_user_password,
        )
        order_designer_user.make_designer()

        clothes.models.OrderClothes.objects.create(
            user=order_user,
            designer=order_designer_user,
            item=self.item1,
            sum=self.item1.cost,
        )
        clothes.models.OrderClothes.objects.create(
            user=order_user,
            designer=order_designer_user,
            item=self.item2,
            sum=self.item2.cost,
        )
        orders = clothes.models.OrderClothes.objects.get_user_orders(
            order_user
        )
        self.assertEqual(len(orders), 2)

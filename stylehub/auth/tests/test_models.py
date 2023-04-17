"""
Tests for auth models

write your model tests here
"""
import clothes.models
import market.models
from auth.models import User
from auth.tests.base import AuthSetup


class TestUser(AuthSetup):
    """Tests for User model"""

    def test_creating_cart(self):
        """tests that cart is creating when user creates"""
        test_username = 'ILOVEDANILAEREMIN'
        e_mail = 'google_danila@gmail.com'
        user = User.objects.create_user(username=test_username, email=e_mail)
        cart = market.models.Cart.objects.get(user=user)
        self.assertTrue(cart)
        test_username = 'ILOVEDANILAEREMIN1'
        e_mail = 'google_danila1@gmail.com'
        superuser = User.objects.create_superuser(
            username=test_username, email=e_mail
        )
        cart = market.models.Cart.objects.get(user=superuser)
        self.assertTrue(cart)

    def test_make_designer(self):
        """testing that user can to be designer"""
        designer_profile = self.user.make_designer()
        self.assertTrue(designer_profile)

    def test_get_lovely_designers(self):
        """tests get_lovely_designers method"""
        user_password = 'trkorerwpoowerpoopo'
        designer_user_password = 'ncxxcvmxcvm231354354'
        user = User.objects.create_user(
            username='testusername',
            email='testemail@gmail.com',
            password=user_password,
        )

        designer_user = User.objects.create_user(
            username='testdesignerusername',
            email='testdesigneruser@gmail.com',
            password=designer_user_password,
        )
        designer_user.make_designer()
        user.lovely.add(designer_user)

        lovely = User.objects.get_lovely_designers(user)
        self.assertEqual(len(lovely), 1)

    def test_get_saved_items(self):
        """tests get_saved_items method"""
        user_password = 'trkorerwpoowerpoopo'
        designer_user_password = 'ncxxcvmxcvm231354354'
        user = User.objects.create_user(
            username='testusername',
            email='testemail@gmail.com',
            password=user_password,
        )

        designer_user = User.objects.create_user(
            username='testdesignerusername',
            email='testdesigneruser@gmail.com',
            password=designer_user_password,
        )
        designer_user.make_designer()

        category_base = market.models.CategoryBase.objects.create(
            name='test_base_category_name'
        )
        category = market.models.CategoryExtended.objects.create(
            name='test_extended_category_name', category_base=category_base
        )
        style = market.models.Style.objects.create(
            name='test_style_name',
        )
        collection = clothes.models.Collection.objects.create(
            name='test_collection_name',
            designer=designer_user,
        )
        item = clothes.models.Item.objects.create(
            designer=designer_user,
            name='test_item_name',
            collection=collection,
            category=category,
            cost=21332345123,
        )
        item.styles.add(style)
        item.save()
        user.saved.add(item)
        user.save()
        saved = User.objects.get_saved_items(user)
        self.assertEqual(len(saved), 1)

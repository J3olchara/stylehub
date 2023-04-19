"""
ENDPOINT market tests

here is endpoint tests
write youth here
"""
from django.test import Client
from django.urls import reverse
from parameterized import parameterized

from core.tests.base import EndpointTests
from market.tests.base import MarketSetUp


class TestEndpoints(EndpointTests, MarketSetUp):
    """Tests endpoints of all views in market app"""

    def test_designer_detail_endpoint(self):
        """Test designer:pk page endpoint"""
        path = reverse('clothes:designer', kwargs={'pk': self.designer1.id})
        client = Client()
        not_auth_resp_get = client.get(path)
        self.assertEqual(
            not_auth_resp_get.status_code,
            200,
            'Не авторизованный пользователь не вошел',
        )
        not_auth_resp_post = client.post(path)
        self.assertEqual(
            not_auth_resp_post.status_code,
            404,
            'Не авторизованный пользователь смог отправить post запрос',
        )

        client.login(username=self.user.username, password=self.user_password)
        logged_user_get_resp = client.get(path)
        self.assertEqual(
            logged_user_get_resp.status_code,
            200,
            'Не авторизованный пользователь не вошел',
        )
        logged_user_post_resp = client.post(path)
        self.assertEqual(
            logged_user_post_resp.status_code,
            404,
            'Не авторизованный пользователь смог отправить post запрос',
        )

        designer_client = Client()
        designer_client.login(
            username=self.designer_user.username,
            password=self.designer_password,
        )
        designer_get_resp = designer_client.get(path)
        self.assertEqual(
            designer_get_resp.status_code,
            200,
            'Дизайнер не смог войти на свою же страницу',
        )
        designer_post_resp = designer_client.post(path)
        self.assertEqual(
            designer_post_resp.status_code,
            302,
            'Дизайнер не может редактировать свой профиль',
        )

    def test_wear_endpoint(self):
        """tests clothes:wear page endpoint"""
        self.endpoint('clothes:wear', pk=self.item1.id)

    def test_collection_detail_endpoint(self):
        """tests clothes:collection_detail page endpoint"""
        self.endpoint('clothes:collection', pk=self.collection1.id)

    def test_recommend_endpoint(self):
        """tests clothes:recommend page endpoint"""
        self.endpoint('clothes:recommend')

    def test_main_endpoint(self):
        """tests clothes:main page endpoint"""
        self.endpoint('clothes:main')

    def test_collections_endpoint(self):
        """tests clothes:collections page endpoint"""
        self.endpoint('clothes:collections')

    def test_designers_endpoint(self):
        """tests clothes:designers page endpoint"""
        self.endpoint('clothes:designers')

    def test_unpopular_endpoint(self):
        """tests clothes:unpopular page endpoint"""
        self.endpoint('clothes:unpopular')

    def test_orders_endpoint(self):
        """tests clothes orders endpoint"""
        self.auth_endpoint('clothes:orders')

    def test_lovely_endpoint(self):
        """tests lovely designers endpoint"""
        self.auth_endpoint('clothes:lovely_designers')

    def test_saved_endpoint(self):
        """tests lovely designers endpoint"""
        self.auth_endpoint('clothes:saved_items')

    @parameterized.expand(
        (
            'collection',
            'item',
        )
    )
    def test_create_endpoint(self, form):
        """tests creation clothes page"""
        self.designer_endpoint('clothes:create', form=form)

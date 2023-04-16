"""
ENDPOINT market tests

here is endpoint tests
write youth here
"""
from django.test import Client
from django.urls import reverse

from market.tests.base import MarketSetUp


class TestEndpoints(MarketSetUp):
    """Tests endpoints of all views in market app"""

    def test_wear_endpoint(self):
        """tests clothes:wear page endpoint"""
        path = reverse('clothes:wear', kwargs={'pk': self.item1.id})
        client = Client()
        resp = client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_collection_detail_endpoint(self):
        """tests clothes:collection_detail page endpoint"""
        path = reverse(
            'clothes:collection_detail', kwargs={'pk': self.collection1.id}
        )
        client = Client()
        resp = client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_designer_detail_endpoint(self):
        """Test designer:pk page endpoint"""
        path = reverse(
            'clothes:designer_detail', kwargs={'pk': self.designer1.id}
        )
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

    def test_recommend_endpoint(self):
        """tests clothes:recommend page endpoint"""
        path = reverse('clothes:recommend')
        client = Client()
        resp = client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_orders_endpoint(self):
        """tests clothes orders endpoint"""
        path = reverse('clothes:orders')
        client = Client()
        not_auth_resp = client.get(path)
        self.assertEqual(not_auth_resp.status_code, 302)
        client.login(username=self.user.username, password=self.user_password)
        auth_resp = client.get(path)
        self.assertEqual(auth_resp.status_code, 200)

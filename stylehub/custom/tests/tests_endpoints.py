from django.test import Client, TestCase
from django.urls import reverse

import auth.models


class TestEndpoints(TestCase):
    def test_custom_home(self):
        user_password = 'kljdfjlksdlkjdljkfjkhfioioiopqwiop'
        desiner_user_password = 'lkfdklknmnbxcvxcmzxc'
        user = auth.models.User.objects.create_user(
            username='test_user',
            email='testusermail@gmail.com',
            password=user_password,
        )
        designer_user = auth.models.User.designers.create_user(
            username='test_desiner_user',
            email='testdesigneremail@ggmail.com',
            password=desiner_user_password,
        )
        path = reverse('custom:home')
        not_auth_client = Client()
        auth_client = Client()
        auth_client.login(username=user.username, password=user_password)
        designer_client = Client()
        not_auth_response = not_auth_client.get(path)
        designer_client.login(
            username=designer_user.username, password=desiner_user_password
        )
        self.assertEqual(not_auth_response.status_code, 302)
        not_desiner_resp = auth_client.get(path)
        self.assertEqual(not_desiner_resp.status_code, 200)
        designer_user_resp = designer_client.get(path)
        self.assertEqual(designer_user_resp.status_code, 200)

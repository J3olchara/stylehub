"""
ENDPOINT market tests

here is endpoint tests
write youth here
"""
from django.test import Client
from django.urls import reverse

import market.models
import market.tests.base


class TestEndpoints(market.tests.base.SetUpBaseClass):
    """Tests endpoints of all views in market app"""

    def test_wear_endpoint(self):
        """tests clothes:wear page endpoint"""
        path = reverse('clothes:wear', kwargs={'pk': self.item1.id})
        client = Client()
        resp = client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_collection_detail_endpoint(self):
        """tests collection:pk page endpoint"""
        path = reverse(
            'clothes:collection_detail', kwargs={'pk': self.collection1.id}
        )
        client = Client()
        resp = client.get(path)
        self.assertEqual(resp.status_code, 200)

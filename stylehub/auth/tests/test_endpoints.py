"""
testing auth endpoints
"""
from core.tests.base import EndpointTests


class TestEndpoints(EndpointTests):
    """tests auth endpoints"""
    def test_signup_endpoint(self):
        """tests auth:signup endpoint"""
        self.endpoint('auth:signup')

    def test_signup_done_endpoint(self):
        """tests auth:signup_done endpoint"""
        self.endpoint('auth:signup_done')

    def test_login_endpoint(self):
        """tests auth:login endpoint"""
        self.endpoint('auth:login')

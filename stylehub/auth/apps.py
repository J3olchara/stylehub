"""AUTH APP SETTINGS"""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """here is app settings"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    label = 'user_auth'

"""APP api config"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """APP api config class"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

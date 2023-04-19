"""API APP SETTINGS"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """here is the app settings"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

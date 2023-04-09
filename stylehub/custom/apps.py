"""custom APP settings"""
from django.apps import AppConfig


class CustomConfig(AppConfig):
    """here is app settings"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom'

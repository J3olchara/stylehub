"""core APP settings"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """here is app settings"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

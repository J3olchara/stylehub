"""STATISTICS APP SETTINGS"""
from django.apps import AppConfig


class StatsConfig(AppConfig):
    """here is app settings"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

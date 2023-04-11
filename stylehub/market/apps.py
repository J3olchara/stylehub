"""Market app settings"""
from django.apps import AppConfig


class MarketConfig(AppConfig):
    """
    Market app config

    write settings variable here
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market'

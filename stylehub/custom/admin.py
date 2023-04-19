"""file for admin models custom app"""
from django.contrib import admin

import custom.models


@admin.register(custom.models.OrderCustomEvaluation)
class AdminOrderCustomEvaluation(
    admin.ModelAdmin[custom.models.OrderCustomEvaluation]
):
    """Admin for realise OrderCustomEvaluation in admin"""

    pass

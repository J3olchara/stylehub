"""market admin models"""

from django.contrib import admin

import market.models


class OrderPictureInline(admin.StackedInline):
    """
    Allows picture to be added to order`s admin panel
    """

    model = market.models.OrderPicture


@admin.register(market.models.OrderCustom)
class OrderCustomAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """
    Admin model order table
    """

    list_display = (
        market.models.OrderCustom.user.field.name,
        market.models.OrderCustom.header.field.name,
        market.models.OrderCustom.max_price.field.name,
    )
    inlines = [
        OrderPictureInline,
    ]
    list_editable = (
        market.models.OrderCustom.header.field.name,
    )

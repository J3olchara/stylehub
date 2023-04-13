"""market admin models"""

from django.contrib import admin

import market.models
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    BaseInline = admin.StackedInline[market.models.OrderPicture, Any]
    BaseModel = admin.ModelAdmin[market.models.OrderCustom]
else:
    BaseInline = admin.StackedInline
    BaseModel = admin.ModelAdmin


class OrderPictureInline(BaseInline):
    """
    Allows picture to be added to order`s admin panel
    """

    model = market.models.OrderPicture


@admin.register(market.models.OrderCustom)
class OrderCustomAdmin(BaseModel):
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
    list_editable = (market.models.OrderCustom.header.field.name,)

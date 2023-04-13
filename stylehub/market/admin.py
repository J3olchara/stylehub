"""auth admin models"""
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.admin.options import TabularInline

import market.models

if TYPE_CHECKING:
    BaseInline = admin.StackedInline[market.models.OrderPicture, Any]
    BaseModel = admin.ModelAdmin[market.models.OrderCustom]
    ItemBaseAdmin = admin.ModelAdmin[market.models.Item]
    StyleBaseAdmin = admin.ModelAdmin[market.models.Style]
    CollectionBaseAdmin = admin.ModelAdmin[market.models.Collection]
    CategoryBasedBaseAdmin = admin.ModelAdmin[market.models.CategoryBase]
    CategoryExtendedBaseAdmin = admin.ModelAdmin[
        market.models.CategoryExtended
    ]
    TabularInlineBaseAdmin = TabularInline[Any, Any]
    OrderClothesBase = admin.ModelAdmin[market.models.OrderClothes]
else:
    BaseInline = admin.StackedInline
    BaseModel = admin.ModelAdmin
    ItemBaseAdmin = admin.ModelAdmin
    StyleBaseAdmin = admin.ModelAdmin
    CollectionBaseAdmin = admin.ModelAdmin
    CategoryBasedBaseAdmin = admin.ModelAdmin
    CategoryExtendedBaseAdmin = admin.ModelAdmin
    TabularInlineBaseAdmin = TabularInline
    OrderClothesBase = admin.ModelAdmin


class ImageAdminInline(TabularInlineBaseAdmin):
    """
    Admin class for realise Item image in ItemAdmin
    """

    extra = 1
    model = market.models.ItemPicture


@admin.register(market.models.Item)
class ItemAdmin(ItemBaseAdmin):
    """
    Item admin for realise Item in admin panel
    """

    inlines = (ImageAdminInline,)
    list_display = (market.models.Item.name.field.name,)
    filter_horizontal = (market.models.Item.styles.field.name,)


@admin.register(market.models.Style)
class StyleAdmin(StyleBaseAdmin):
    """
    Style admin for realise Style in admin panel
    """

    pass


@admin.register(market.models.Collection)
class CollectionAdmin(CollectionBaseAdmin):
    """
    Collection admin for realise Collection in admin panel
    """

    pass


@admin.register(market.models.CategoryBase)
class CategoryBasedAdmin(CategoryBasedBaseAdmin):
    """
    CategoryBased admin for realise CategoryBased in admin panel
    """

    pass


@admin.register(market.models.CategoryExtended)
class CategoryExtendedAdmin(CategoryExtendedBaseAdmin):
    """
    CategoryExtended admin for realise CategoryExtended in admin panel
    """

    pass


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


@admin.register(market.models.OrderClothes)
class OrderClothesAdmin(OrderClothesBase):
    """
    admin model of clothes orders
    """

    list_display = (
        market.models.OrderClothes.user.field.name,
        market.models.OrderClothes.designer.field.name,
        market.models.OrderClothes.sum.field.name,
        market.models.OrderClothes.item.field.name,
        market.models.OrderClothes.status.field.name,
    )

    list_editable = (market.models.OrderClothes.status.field.name,)

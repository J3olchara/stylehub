"""auth admin models"""
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.admin.options import TabularInline

from market.models import (
    CategoryBase,
    CategoryExtended,
    Collection,
    Item,
    ItemPicture,
    Style,
)

if TYPE_CHECKING:
    BaseInline = admin.StackedInline[market.models.OrderPicture, Any]
    BaseModel = admin.ModelAdmin[market.models.OrderCustom]
    ItemBaseAdmin = admin.ModelAdmin[Item]
    StyleBaseAdmin = admin.ModelAdmin[Style]
    CollectionBaseAdmin = admin.ModelAdmin[Collection]
    CategoryBasedBaseAdmin = admin.ModelAdmin[CategoryBase]
    CategoryExtendedBaseAdmin = admin.ModelAdmin[CategoryExtended]
    TabularInlineBaseAdmin = TabularInline[Any, Any]
else:
    BaseInline = admin.StackedInline
    BaseModel = admin.ModelAdmin
    ItemBaseAdmin = admin.ModelAdmin
    StyleBaseAdmin = admin.ModelAdmin
    CollectionBaseAdmin = admin.ModelAdmin
    CategoryBasedBaseAdmin = admin.ModelAdmin
    CategoryExtendedBaseAdmin = admin.ModelAdmin
    TabularInlineBaseAdmin = TabularInline


class ImageAdminInline(TabularInlineBaseAdmin):
    """
    Admin class for realise Item image in ItemAdmin
    """

    extra = 1
    model = ItemPicture


@admin.register(Item)
class ItemAdmin(ItemBaseAdmin):
    """
    Item admin for realise Item in admin panel
    """

    inlines = (ImageAdminInline,)
    list_display = (Item.name.field.name,)
    filter_horizontal = (Item.styles.field.name,)


@admin.register(Style)
class StyleAdmin(StyleBaseAdmin):
    """
    Style admin for realise Style in admin panel
    """

    pass


@admin.register(Collection)
class CollectionAdmin(CollectionBaseAdmin):
    """
    Collection admin for realise Collection in admin panel
    """

    pass


@admin.register(CategoryBase)
class CategoryBasedAdmin(CategoryBasedBaseAdmin):
    """
    CategoryBased admin for realise CategoryBased in admin panel
    """

    pass


@admin.register(CategoryExtended)
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


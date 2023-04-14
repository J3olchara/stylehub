"""auth admin models"""
from django.contrib import admin
from django.contrib.admin.options import TabularInline

import market.models


class ImageAdminInline(
    TabularInline[market.models.ItemPicture, market.models.Item]
):
    """
    Admin class for realise Item image in ItemAdmin
    """

    extra = 1
    model = market.models.ItemPicture


@admin.register(market.models.Item)
class ItemAdmin(admin.ModelAdmin[market.models.Item]):
    """
    Item admin for realise Item in admin panel
    """

    inlines = (ImageAdminInline,)
    list_display = (market.models.Item.name.field.name,)
    filter_horizontal = (market.models.Item.styles.field.name,)


@admin.register(market.models.Style)
class StyleAdmin(admin.ModelAdmin[market.models.Style]):
    """
    Style admin for realise Style in admin panel
    """

    list_display = (
        'id',
        market.models.Style.name.field.name,
    )
    list_editable = (market.models.Style.name.field.name,)
    readonly_fields = (market.models.Style.slug.field.name,)


@admin.register(market.models.Collection)
class CollectionAdmin(admin.ModelAdmin[market.models.Collection]):
    """
    Collection admin for realise Collection in admin panel
    """

    pass


@admin.register(market.models.CategoryBase)
class CategoryBaseAdmin(admin.ModelAdmin[market.models.CategoryBase]):
    """
    CategoryBased admin for realise CategoryBased in admin panel
    """

    list_display = (
        'id',
        market.models.CategoryBase.name.field.name,
    )
    list_editable = (market.models.CategoryBase.name.field.name,)
    readonly_fields = (market.models.CategoryBase.slug.field.name,)


@admin.register(market.models.CategoryExtended)
class CategoryExtendedAdmin(admin.ModelAdmin[market.models.CategoryExtended]):
    """
    CategoryExtended admin for realise CategoryExtended in admin panel
    """

    list_display = (
        'id',
        market.models.CategoryExtended.name.field.name,
        market.models.CategoryExtended.category_base.field.name,
    )
    list_editable = (market.models.CategoryExtended.name.field.name,)
    readonly_fields = (market.models.CategoryExtended.slug.field.name,)


class OrderPictureInline(
    admin.StackedInline[market.models.OrderPicture, market.models.OrderCustom]
):
    """
    Allows picture to be added to order`s admin panel
    """

    model = market.models.OrderPicture


@admin.register(market.models.OrderCustom)
class OrderCustomAdmin(admin.ModelAdmin[market.models.OrderCustom]):
    """
    Admin model order table
    """

    list_display = (
        market.models.OrderCustom.user.field.name,
        market.models.OrderCustom.header.field.name,
        market.models.OrderCustom.max_price.field.name,
    )
    inlines = (OrderPictureInline,)
    list_editable = (market.models.OrderCustom.header.field.name,)

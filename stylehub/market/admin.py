"""auth admin models"""
from django.contrib import admin
from django.contrib.admin.options import TabularInline

import clothes.models
import custom.models
import market.models


class ImageAdminInline(
    TabularInline[clothes.models.ItemPicture, clothes.models.Item]
):
    """
    Admin class for realise Item image in ItemAdmin
    """

    extra = 1
    model = clothes.models.ItemPicture


@admin.register(clothes.models.Item)
class ItemAdmin(admin.ModelAdmin[clothes.models.Item]):
    """
    Item admin for realise Item in admin panel
    """

    inlines = (ImageAdminInline,)
    list_display = (clothes.models.Item.name.field.name,)
    filter_horizontal = (clothes.models.Item.styles.field.name,)


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


@admin.register(clothes.models.Collection)
class CollectionAdmin(admin.ModelAdmin[clothes.models.Collection]):
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
    admin.StackedInline[
        custom.models.OrderCustomPicture, custom.models.OrderCustom
    ]
):
    """
    Allows picture to be added to order`s admin panel
    """

    model = custom.models.OrderCustomPicture


@admin.register(custom.models.OrderCustom)
class OrderCustomAdmin(admin.ModelAdmin[custom.models.OrderCustom]):
    """
    Admin model order table
    """

    list_display = (
        custom.models.OrderCustom.user.field.name,
        custom.models.OrderCustom.header.field.name,
        custom.models.OrderCustom.max_price.field.name,
    )
    inlines = (OrderPictureInline,)
    list_editable = (custom.models.OrderCustom.header.field.name,)


@admin.register(clothes.models.OrderClothes)
class OrderClothesAdmin(admin.ModelAdmin[clothes.models.OrderClothes]):
    """
    Admin model order table
    """

    list_display = (
        clothes.models.OrderClothes.user.field.name,
        clothes.models.OrderClothes.designer.field.name,
        clothes.models.OrderClothes.sum.field.name,
        clothes.models.OrderClothes.item.field.name,
        clothes.models.OrderClothes.status.field.name,
        clothes.models.OrderClothes.edited.field.name,
    )

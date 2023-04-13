"""auth admin models"""
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.models import DesignerProfile, User
import market.models


if TYPE_CHECKING:
    DesignerBaseAdmin = admin.ModelAdmin[DesignerProfile]
    CartInline = admin.TabularInline[Any, Any]
else:
    DesignerBaseAdmin = admin.ModelAdmin
    CartInline = admin.TabularInline


@admin.register(DesignerProfile)
class DesignerProfileAdmin(DesignerBaseAdmin):
    """class for see Designer model in Admin"""

    pass


class UserCartInline(CartInline):
    model = market.models.Cart
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = (UserCartInline, )


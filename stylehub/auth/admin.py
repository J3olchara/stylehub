"""auth admin models"""
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

import auth.models
import market.models

if TYPE_CHECKING:
    DesignerBaseAdmin = admin.ModelAdmin[auth.models.DesignerProfile]
    CartInline = admin.TabularInline[Any, Any]
else:
    DesignerBaseAdmin = admin.ModelAdmin
    CartInline = admin.TabularInline


@admin.register(auth.models.DesignerProfile)
class DesignerProfileAdmin(DesignerBaseAdmin):
    """class for see Designer model in Admin"""

    pass


class UserCartInline(CartInline):
    """Inline cart field for User"""

    model = market.models.Cart
    can_delete = False


@admin.register(auth.models.User)
class UserAdmin(UserAdminBase):
    """User admin model"""

    inlines = (UserCartInline,)

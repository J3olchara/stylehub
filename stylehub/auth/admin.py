"""auth admin models"""
from typing import TYPE_CHECKING, Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase

import market.models
from auth.models import DesignerProfile, User

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
    """Inline cart field for User"""

    model = market.models.Cart
    can_delete = False


@admin.register(User)
class UserAdmin(UserAdminBase):
    """User admin model"""

    inlines = (UserCartInline,)

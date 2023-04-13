"""auth admin models"""
from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.models import DesignerProfile, User

admin.site.register(User, UserAdmin)


if TYPE_CHECKING:
    DesignerBaseAdmin = admin.ModelAdmin[DesignerProfile]
else:
    DesignerBaseAdmin = admin.ModelAdmin


@admin.register(DesignerProfile)
class DesignerProfileAdmin(DesignerBaseAdmin):
    """class for see Designer model in Admin"""

    pass

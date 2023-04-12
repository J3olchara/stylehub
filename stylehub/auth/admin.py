"""auth admin models"""
from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.models import Designer, User

admin.site.register(User, UserAdmin)


if TYPE_CHECKING:
    DesignerBaseAdmin = admin.ModelAdmin[Designer]
else:
    DesignerBaseAdmin = admin.ModelAdmin


@admin.register(Designer)
class DesignerAdmin(DesignerBaseAdmin):
    """class for see Designer model in Admin"""

    pass

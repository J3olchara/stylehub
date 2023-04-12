"""auth admin models"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.models import Designer, User

admin.site.register(User, UserAdmin)  # type: ignore[arg-type]


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    pass

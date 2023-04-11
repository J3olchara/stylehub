"""auth admin models"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth.models import User

admin.register(User, UserAdmin)  # type: ignore[arg-type]

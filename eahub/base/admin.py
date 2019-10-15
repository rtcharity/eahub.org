from authtools import admin as authtools_admin
from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(authtools_admin.UserAdmin):
    list_display = [
        "is_active",
        "email",
        "profile",
        "is_superuser",
        "is_staff",
        "date_joined",
    ]
    list_display_links = ["email", "profile"]
    search_fields = ["email", "profile__name"]
    ordering = ["-date_joined"]

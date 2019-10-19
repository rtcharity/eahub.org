import django_admin_relation_links
from authtools import admin as authtools_admin
from django.contrib import admin

from ..profiles import models as profiles_models
from . import models


@admin.register(models.User)
class UserAdmin(
    django_admin_relation_links.AdminChangeLinksMixin, authtools_admin.UserAdmin
):
    list_select_related = ["profile"]
    list_display = [
        "is_active",
        "email",
        "profile_link",
        "is_profile_approved",
        "date_joined",
        "is_superuser",
        "is_staff",
    ]
    change_links = ["profile"]
    list_filter = ["is_superuser", "is_staff", "is_active", "profile__is_approved"]
    search_fields = ["email", "profile__name"]
    ordering = ["-date_joined"]
    actions = ["approve_profiles"]

    def is_profile_approved(self, user):
        try:
            profile = user.profile
        except profiles_models.Profile.DoesNotExist:
            return None
        return profile.is_approved

    is_profile_approved.short_description = "Approved?"
    is_profile_approved.boolean = True

    def approve_profiles(self, request, queryset):
        profiles_models.Profile.objects.filter(user__in=queryset).update(
            is_approved=True
        )

    approve_profiles.short_description = "Approve selected users' profiles"
    approve_profiles.allowed_permissions = ["change"]

from typing import Optional

import django_admin_relation_links
from authtools import admin as authtools_admin
from django.contrib import admin
from enumfields.admin import EnumFieldListFilter
from rangefilter.filter import DateRangeFilter
from solo.admin import SingletonModelAdmin

from eahub.base import models
from eahub.base.models import User
from eahub.profiles.models import Profile


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
        "last_login",
        "is_superuser",
        "is_staff",
        "profile_visibility",
    ]
    change_links = ["profile"]
    list_filter = [
        "is_superuser",
        "is_staff",
        "is_active",
        "profile__is_approved",
        ("profile__visibility", EnumFieldListFilter),
        ("date_joined", DateRangeFilter),
        ("last_login", DateRangeFilter),
    ]
    search_fields = ["email", "profile__first_name", "profile__last_name"]
    actions = ["approve_profiles"]

    def is_profile_approved(self, user):
        profile = get_profile(user)
        if profile is None:
            return profile
        return profile.is_approved

    is_profile_approved.short_description = "Approved?"
    is_profile_approved.boolean = True

    def approve_profiles(self, request, queryset):
        Profile.objects.filter(user__in=queryset).update(is_approved=True)

    approve_profiles.short_description = "Approve selected users' profiles"
    approve_profiles.allowed_permissions = ["change"]

    def profile_visibility(self, user):
        profile = get_profile(user)
        if profile is None:
            return profile
        return profile.visibility

    profile_visibility.short_description = "Profile Visibility"


def get_profile(user: User) -> Optional[Profile]:
    try:
        return user.profile
    except Profile.DoesNotExist:
        return None


@admin.register(models.MessagingLog)
class MessagingLogAdmin(admin.ModelAdmin):
    list_display = [
        "sender_email",
        "recipient_email",
        "recipient_type",
        "send_action_uuid",
        "time",
    ]
    list_filter = [
        "recipient_type",
        ("time", DateRangeFilter),
    ]
    search_fields = ["sender", "recipient"]


admin.site.register(models.FeedbackURLConfig, SingletonModelAdmin)

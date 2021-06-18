from typing import Optional

import django_admin_relation_links
from adminutils import options
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
        "get_visibility",
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

    @options(desc="Approved", boolean=True)
    def is_profile_approved(self, user) -> Optional[bool]:
        profile = get_profile(user)
        if profile is None:
            return None
        return profile.is_approved

    @options(desc="Visibility")
    def get_visibility(self, user) -> str:
        profile = get_profile(user)
        if profile is None:
            return ""
        return profile.visibility.value


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

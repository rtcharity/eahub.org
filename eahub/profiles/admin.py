from adminutils import options
from allauth.account.models import EmailAddress
from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from rangefilter.filter import DateRangeFilter

from eahub.profiles.models import (
    GivingPledge,
    Profile,
    ProfileAnalyticsLog,
    ProfileSlug,
)

from ..base import utils


class GivingPledgesFilter(admin.SimpleListFilter):
    title = "giving pledges"
    parameter_name = "giving_pledge"

    def lookups(self, request, model_admin):
        return GivingPledge.choices()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(giving_pledges__contains=[self.value()])
        else:
            return queryset


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv", "approve_profiles"]
    model = Profile
    list_display = (
        "email",
        "name",
        "is_approved",
        "is_email_verified",
        "personal_website_url",
        "summary",
        "cause_areas_other",
        "giving_pledges_readable",
        "is_public",
        "date_joined",
    )
    list_filter = [
        "user__emailaddress__verified",
        "is_approved",
        "is_public",
        "email_visible",
        "available_to_volunteer",
        "user__date_joined",
        GivingPledgesFilter,
    ]
    search_fields = ["user__email", "name"]
    ordering = ["-user__date_joined"]

    def export_csv(self, request, queryset):
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, Profile, "profiles"
        )

    @options(desc="Giving Pledges", order="profile.giving_pledges")
    def giving_pledges_readable(self, obj: Profile):
        return obj.get_pretty_giving_pledges()

    @options(desc="email", order="user__email")
    def email(self, obj: Profile):
        return obj.user.email

    @options(desc="email checked", order="user__emailaddress__verified", boolean=True)
    def is_email_verified(self, obj: Profile):
        return EmailAddress.objects.filter(
            user=obj.user,
            verified=True,
        ).exists()

    @options(desc="date joined", order="user__date_joined")
    def date_joined(self, obj: Profile):
        return obj.user.date_joined

    @options(desc="Approve selected profiles", allowed_permissions=["change"])
    def approve_profiles(self, request, queryset):
        queryset.update(is_approved=True)


class ProfileAnalyticsResource(ModelResource):
    class Meta:
        model = ProfileAnalyticsLog
        export_order = [
            "id",
            "profile",
            "time",
            "action",
            "action_uuid",
            "field",
            "new_value",
            "old_value",
        ]


@admin.register(ProfileAnalyticsLog)
class ProfileAnalyticsAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        "profile",
        "time",
        "action",
        "action_uuid",
        "field",
        "new_value",
        "old_value",
    )
    list_filter = ["action", ("time", DateRangeFilter)]
    search_fields = [
        "profile__user__email",
        "profile__name",
        "action",
        "field",
        "old_value",
        "new_value",
    ]
    ordering = ["-time"]
    resource_class = ProfileAnalyticsResource


admin.site.register(ProfileSlug)

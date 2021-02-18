from adminutils import options
from allauth.account.models import EmailAddress
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from rangefilter.filter import DateRangeFilter

from eahub.base import utils
from eahub.base.models import User
from eahub.profiles.models import (
    GivingPledge,
    Profile,
    ProfileAnalyticsLog,
    ProfileSlug,
    ProfileTag,
    ProfileTagType,
)


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
    actions = ["export_csv", "approve_profiles", "delete_profiles_and_users"]
    model = Profile
    list_display = (
        "email",
        "name",
        "is_approved",
        "is_email_verified",
        "personal_website_url",
        "summary",
        "cause_areas_other",
        "expertise_areas_other",
        "looking_for",
        "offering",
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

    def get_actions(self, request: HttpRequest) -> dict:
        actions: dict = super().get_actions(request)
        del actions["delete_selected"]
        return actions

    def export_csv(
        self, request: HttpRequest, queryset: QuerySet, **kwargs
    ) -> HttpResponse:
        return utils.ExportCsvMixin.export_csv(
            self,
            request=request,
            queryset=queryset,
            model=Profile,
            filename="profiles",
        )

    @options(desc="Giving Pledges", order="profile.giving_pledges")
    def giving_pledges_readable(self, obj: Profile):
        return obj.get_pretty_giving_pledges()

    @options(desc="email", order="user__email")
    def email(self, obj: Profile):
        return obj.user.email

    @options(desc="email checked", order="user__emailaddress__verified", boolean=True)
    def is_email_verified(self, obj: Profile) -> bool:
        return EmailAddress.objects.filter(user=obj.user, verified=True).exists()

    @options(desc="date joined", order="user__date_joined")
    def date_joined(self, obj: Profile):
        return obj.user.date_joined

    @options(desc="Approve selected profiles", allowed_permissions=["change"])
    def approve_profiles(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(is_approved=True)

    @options(desc="Delete selected profiles & users", allowed_permissions=["delete"])
    def delete_profiles_and_users(self, request: HttpRequest, queryset: QuerySet):
        user_queryset = User.objects.filter(
            profile__pk__in=queryset.values_list("pk", flat=True)
        )
        count = user_queryset.count()
        user_queryset.delete()
        messages.success(request, f"Deleted '{count}' users & their profiles.")


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


@admin.register(ProfileTagType)
class ProfileTagTypeAdmin(admin.ModelAdmin):
    list_display = [
        "type",
    ]


@admin.register(ProfileTag)
class ProfileTagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "author",
        "description",
        "is_verified",
        "created_at",
    ]
    filter_horizontal = [
        "types",
    ]
    list_filter = [
        "types",
        "is_verified",
        "created_at",
    ]


admin.site.register(ProfileSlug)

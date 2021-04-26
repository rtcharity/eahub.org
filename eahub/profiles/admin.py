from adminutils import options
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.models import EmailAddress
from allauth.account.utils import user_pk_to_url_str
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse
from django_object_actions import DjangoObjectActions
from enumfields.admin import EnumFieldListFilter
from import_export.admin import ImportExportMixin
from rangefilter.filter import DateRangeFilter

from eahub.base.models import User
from eahub.profiles.legacy import GivingPledge
from eahub.profiles.models import (
    Profile,
    ProfileAnalyticsLog,
    ProfileSlug,
    ProfileTag,
    ProfileTagType,
)
from eahub.profiles.resources import ProfileAnalyticsResource, ProfileResource


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
class ProfileAdmin(ImportExportMixin, DjangoObjectActions, admin.ModelAdmin):
    actions = ["approve_profiles", "delete_profiles_and_users"]
    model = Profile
    resource_class = ProfileResource
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_approved",
        "is_email_verified",
        "personal_website_url",
        "summary",
        "cause_areas_other",
        "expertise_areas_other",
        "looking_for",
        "offering",
        "visibility",
        "date_joined",
    )
    list_filter = [
        "user__emailaddress__verified",
        "is_approved",
        "email_visible",
        "available_to_volunteer",
        "user__date_joined",
        GivingPledgesFilter,
        ("visibility", EnumFieldListFilter),
    ]
    search_fields = [
        "user__email",
        "first_name",
        "last_name",
    ]
    ordering = ["-user__date_joined"]
    filter_horizontal = [
        "tags_generic",
        "tags_cause_area",
        "tags_expertise_area",
        "tags_organisational_affiliation",
        "tags_speech_topic",
        "tags_pledge",
    ]
    
    change_actions = [
        "generate_password_reset_link",
    ]

    def get_actions(self, request: HttpRequest) -> dict:
        actions: dict = super().get_actions(request)
        del actions["delete_selected"]
        return actions

    def generate_password_reset_link(self, request: HttpRequest, obj: Profile):
        token_generator = EmailAwarePasswordResetTokenGenerator()
        url = reverse(
            "profile_import_password_set",
            kwargs=dict(
                uidb36=user_pk_to_url_str(obj.user),
                key=token_generator.make_token(obj.user),
            ),
        )
        return HttpResponse(url)

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
        "profile__first_name",
        "profile__last_name",
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
        "synonyms",
        "description",
        "get_types_formatted",
        "status",
        "author",
        "is_featured",
        "created_at",
        "count",
    ]
    filter_horizontal = [
        "types",
    ]
    list_filter = [
        "types",
        "status",
        "is_featured",
        "created_at",
    ]
    search_fields = [
        "name",
        "synonyms",
        "description",
        "author__user__email",
        "author__name",
    ]

    @options(desc="types")
    def get_types_formatted(self, instance: ProfileTag) -> str:
        type_list = [str(type_instance.type) for type_instance in instance.types.all()]
        return ", ".join(type_list)


admin.site.register(ProfileSlug)

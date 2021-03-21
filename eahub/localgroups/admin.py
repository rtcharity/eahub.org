from typing import List, Optional

from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db.models import Value
from django.db.models.functions import Concat
from import_export import fields, widgets
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from rangefilter.filter import DateRangeFilter

from eahub.base.models import User
from eahub.base.utils import ExportCsvMixin
from eahub.localgroups.models import LocalGroup, LocalGroupType, Organisership
from eahub.profiles.models import Profile


class EnumArrayWidget(widgets.Widget):
    """
    Widget for an Array field. Can be used for Postgres' Array field.
    :param separator: Defaults to ``','``
    """

    def __init__(self, separator=None):
        if separator is None:
            separator = ","
        self.separator = separator
        super().__init__()

    def clean(self, value, row=None, *args, **kwargs):
        return value

    def render(self, value, obj=None):
        return self.separator.join(str(v) for v in value)


class LocalGroupResource(ModelResource):
    organisers_dehydrated = fields.Field(column_name="organisers")
    local_group_types_dehydrated = fields.Field(column_name="types")

    class Meta:
        model = LocalGroup
        import_id_fields = ("id",)
        export_order = [
            "id",
            "name",
            "slug",
            "is_active",
            "is_public",
            "organisers_freetext",
            "email",
            "local_group_types_dehydrated",
            "city_or_town",
            "country",
            "lat",
            "lon",
            "website",
            "other_website",
            "facebook_group",
            "facebook_page",
            "meetup_url",
            "airtable_record",
            "last_edited",
            "other_info",
        ]

    @classmethod
    def widget_from_django_field(cls, f, default=widgets.Widget):
        if isinstance(f, ArrayField):
            return EnumArrayWidget
        else:
            return super().widget_from_django_field(f)

    def import_row(
        self,
        row,
        instance_loader,
        using_transactions=True,
        dry_run=False,
        raise_errors=False,
        **kwargs,
    ):
        row = self.remove_bom_from_row_keys(row)
        return super().import_row(
            row, instance_loader, using_transactions, dry_run, raise_errors, **kwargs
        )

    def before_import_row(self, row: dict, **kwargs) -> dict:
        row["local_group_types"] = [
            type
            for type in self.hydrate_local_group_types(row["types"])
            if type is not None
        ]
        organisers_users, organisers_non_users = self.hydrate_organisers(row)
        row["organisers"] = ",".join(map(lambda x: str(x.id), organisers_users))
        row["organisers_freetext"] = ",".join(organisers_non_users)

        return super().before_import_row(row, **kwargs)

    def hydrate_local_group_type(self, group_type_raw: str) -> Optional[LocalGroupType]:
        for key, value in LocalGroupType.labels.items():
            if value == group_type_raw.strip():
                return key
        return None

    def hydrate_organiser(self, organiser_raw: str, row: dict) -> Optional[User]:
        profiles = (
           Profile.objects
               .annotate(full_name=Concat("first_name", "last_name"))
               .filter(first_name=organiser_raw)
        )
        if len(profiles) == 1:
            return profiles[0].user
        elif len(profiles) > 1:
            group_id = row["id"]
            organisers = []
            for profile in profiles:
                organisership = Organisership.objects.filter(
                    local_group_id=group_id, user=profile.user
                )
                if organisership:
                    organisers.append(profile)
            if len(organisers) > 0:
                organisers.sort(key=lambda x: x.user.date_joined, reverse=True)
                return organisers[0].user
            else:
                return None
        else:
            return None

    def hydrate_local_group_types(
        self, group_types_raw: str
    ) -> Optional[List[LocalGroupType]]:
        group_types = []
        for group_type_raw in group_types_raw.split(","):
            group_types.append(self.hydrate_local_group_type(group_type_raw))

        return group_types if group_types else None

    def hydrate_organisers(
        self, row: dict
    ) -> (Optional[List[User]], Optional[List[str]]):
        users = []
        non_users = []
        organisers_raw = row["organisers_names"]
        for organiser_raw in organisers_raw.split(","):
            user = self.hydrate_organiser(organiser_raw, row)
            if user:
                users.append(user)
            else:
                non_users.append(organiser_raw)

        return (users, non_users)

    def remove_bom_from_row_keys(self, row):
        new_row = {}
        bom = "\ufeff"
        for key in row:
            if bom in key:
                new_key = key.replace(bom, "")
                new_row[new_key] = row[key]
            else:
                new_row[key] = row[key]
        return new_row


@admin.register(LocalGroup)
class LocalGroupAdmin(ImportExportMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_csv", "make_public", "make_not_public"]
    list_display = [
        "name",
        "local_group_type",
        "is_active",
        "is_public",
        "city_or_town",
        "country",
        "email",
        "last_edited",
    ]
    list_filter = [
        "is_public",
        "is_active",
        "local_group_type",
        "last_edited",
        "country",
        "local_group_types",
        ("last_edited", DateRangeFilter),
    ]
    search_fields = [
        "name",
        "slug",
        "organisers__email",
        "city_or_town",
        "website",
        "other_website",
        "email",
        "meetup_url",
        "other_info",
    ]
    resource_class = LocalGroupResource

    def export_csv(self, request, queryset, **kwargs):
        return ExportCsvMixin.export_csv(
            self, request, queryset, LocalGroup, "localgroups"
        )

    def make_public(self, request, queryset, **kwargs):
        queryset.update(is_public=True)

    def make_not_public(self, request, queryset, **kwargs):
        queryset.update(is_public=False)

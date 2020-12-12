from typing import List, Optional

from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from import_export import fields
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget
from import_export import widgets

from eahub.base.models import User
from eahub.base.utils import ExportCsvMixin
from eahub.localgroups.models import LocalGroup, LocalGroupType

import ipdb;

class EnumArrayWidget(widgets.Widget):
    """
    Widget for an Array field. Can be used for Postgres' Array field.
    :param separator: Defaults to ``','``
    """

    def __init__(self, separator=None):
        if separator is None:
            separator = ','
        self.separator = separator
        super().__init__()

    def clean(self, value, row=None, *args, **kwargs):
        return value

    def render(self, value, obj=None):
        return self.separator.join(str(v) for v in value)


class LocalGroupResource(ModelResource):
    organisers = fields.Field(
        widget=ManyToManyWidget(User, field="email"), attribute="organisers"
    )
    local_group_type_dehydrated = fields.Field(column_name="type")
    local_group_types_dehydrated = fields.Field(column_name="types")

    class Meta:
        model = LocalGroup
        export_order = [
            "id",
            "name",
            "slug",
            "is_active",
            "is_public",
            "organisers",
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

    def before_import_row(self, row: dict, **kwargs) -> dict:
        row["local_group_types"] = self.hydrate_local_group_types(row["types"])
        return super().before_import_row(row, **kwargs)

    def dehydrate_local_group_type_dehydrated(self, group: LocalGroup) -> str:
        if group.local_group_type:
            return LocalGroupType.labels[group.local_group_type]
        else:
            return ""

    def hydrate_local_group_type(self, group_type_raw: str) -> Optional[LocalGroupType]:
        for key, value in LocalGroupType.labels.items():
            if value == group_type_raw.strip():
                return key
        return None

    def dehydrate_local_group_types_dehydrated(self, group: LocalGroup) -> str:
        if group.local_group_types:
            ", ".join(map(LocalGroupType.label, group.local_group_types))
        else:
            return ""

    def hydrate_local_group_types(
        self, group_types_raw: str
    ) -> Optional[List[LocalGroupType]]:
        group_types = []
        for group_type_raw in group_types_raw.split(","):
            group_types.append(self.hydrate_local_group_type(group_type_raw))

        return group_types if group_types else None


@admin.register(LocalGroup)
class LocalGroupAdmin(ImportExportMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_csv"]
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
        meta = LocalGroup._meta
        fieldnames = [
            field.name
            for field in meta.fields + meta.many_to_many
            if field.name != "local_group_type"
        ]
        fieldnames.append("organisers_emails")
        return ExportCsvMixin.export_csv(
            self, request, queryset, fieldnames, "localgroups"
        )



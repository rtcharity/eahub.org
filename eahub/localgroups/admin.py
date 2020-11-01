from typing import List

from django.contrib import admin
from import_export import fields
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget

from eahub.base.models import User
from eahub.base.utils import ExportCsvMixin
from eahub.localgroups.models import LocalGroup
from eahub.localgroups.models import LocalGroupType


class LocalGroupResource(ModelResource):
    organisers = fields.Field(
        widget=ManyToManyWidget(User, field='email'),
        attribute='organisers',
    )

    class Meta:
        model = LocalGroup
        export_order = [
            'id',
            'name',
            'slug',
            'is_active',
            'is_public',
            'organisers',
            'organisers_freetext',
            'email',
            'local_group_type',
            'local_group_types',
            'city_or_town',
            'country',
            'lat',
            'lon',
            'website',
            'other_website',
            'facebook_group',
            'facebook_page',
            'email',
            'meetup_url',
            'airtable_record',
            'last_edited',
            'other_info',
        ]

    def dehydrate_local_group_type(self, group: LocalGroup) -> str:
        if group.local_group_type:
            return LocalGroupType.labels[group.local_group_type]
        else:
            return ''

    def hydrate_local_group_type(self, group_type_raw: str) -> LocalGroupType:
        for key, value in LocalGroupType.labels:
            if value == group_type_raw.strip():
                return key

    def dehydrate_local_group_types(self, group: LocalGroup) -> str:
        if group.local_group_types:
            ', '.join(map(LocalGroupType.label, group.local_group_types))
        else:
            return ''

    def hydrate_local_group_types(self, group_types_raw: str) -> List[LocalGroupType]:
        group_types = []
        for group_type_raw in group_types_raw.split(','):
            group_types.append(
                self.hydrate_local_group_type(group_type_raw)
            )
        return group_types


@admin.register(LocalGroup)
class LocalGroupAdmin(ImportExportMixin, admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_csv"]
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

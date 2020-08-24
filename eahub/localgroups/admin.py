from django.contrib import admin

from ..base import utils
from . import models


class LocalGroupAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        meta = models.LocalGroup._meta
        fieldnames = [
            field.name
            for field in meta.fields + meta.many_to_many
            if field.name != "local_group_type"
        ]
        fieldnames.append("organisers_emails")
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, fieldnames, "localgroups"
        )


admin.site.register(models.LocalGroup, LocalGroupAdmin)

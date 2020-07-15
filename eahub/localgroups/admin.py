from django.contrib import admin

from . import models
from ..base import utils


class LocalGroupAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, models.LocalGroup._meta, ["local_group_type"]
        )


admin.site.register(models.LocalGroup, LocalGroupAdmin)

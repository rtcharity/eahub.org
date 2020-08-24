from django.contrib import admin

from ..base import utils
from . import models


class ProfileAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv"]

    def export_csv(self, request, queryset):
        meta = models.Profile._meta
        fieldnames = [field.name for field in meta.fields + meta.many_to_many]
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, fieldnames, "profiles"
        )


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileSlug)

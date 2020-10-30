from django.contrib import admin

from ..base import utils
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv"]
    list_display = [
        "name",
        "is_public",
        "is_approved",
        "country",
        "available_to_volunteer",
    ]
    list_filter = [
        "is_approved",
        "is_public",
        "available_to_volunteer",
    ]
    search_fields = [
        "user__email",
        "name",
    ]
    ordering = ["-user__date_joined"]

    def export_csv(self, request, queryset):
        meta = models.Profile._meta
        fieldnames = [field.name for field in meta.fields + meta.many_to_many]
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, fieldnames, "profiles"
        )


admin.site.register(models.ProfileSlug)

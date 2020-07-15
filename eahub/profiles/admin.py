from django.contrib import admin

from . import models
from ..base import utils

class ProfileAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        return utils.ExportCsvMixin.export_csv(self,request,queryset, models.Profile._meta)


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileSlug)
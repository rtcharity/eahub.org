from django.contrib import admin

from ..base import utils
from . import models


class GivingPledgesFilter(admin.SimpleListFilter):
    title = 'giving_pledges_readable'
    parameter_name = 'giving_pledge'

    def lookups(self, request, model_admin):
        return models.GivingPledge.choices()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(giving_pledges__contains=[self.value()])
        else:
            return queryset


class ProfileAdmin(admin.ModelAdmin, utils.ExportCsvMixin):
    actions = ["export_csv"]
    model = models.Profile
    list_display = (
        "name",
        "is_public",
        "is_approved",
        "country",
        "available_to_volunteer",
        "giving_pledges_readable"
    )
    list_filter = [GivingPledgesFilter, "is_approved", "is_public", "available_to_volunteer"]
    search_fields = ["user__email", "name"]
    ordering = ["-user__date_joined"]

    def export_csv(self, request, queryset):
        meta = models.Profile._meta
        fieldnames = [field.name for field in meta.fields + meta.many_to_many]
        return utils.ExportCsvMixin.export_csv(
            self, request, queryset, fieldnames, "profiles"
        )

    def giving_pledges_readable(self, obj):
        return obj.get_pretty_giving_pledges()

    giving_pledges_readable.short_description = "Giving Pledges"
    giving_pledges_readable.admin_order_field = 'profile.giving_pledges'

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.ProfileSlug)

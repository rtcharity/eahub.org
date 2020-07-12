from django.contrib import admin

import csv
from django.http import HttpResponse

from . import models

class LocalGroupAdmin(admin.ModelAdmin):
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        meta = models.LocalGroup._meta
        field_names = [field.name for field in meta.fields if field.name != "local_group_type"]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow(obj.convert_to_row(field_names))

        return response

    export_csv.short_description = "Export as CSV"


admin.site.register(models.LocalGroup, LocalGroupAdmin)
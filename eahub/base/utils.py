import csv

import environ
from django.http import HttpResponse

from eahub.profiles import models


def user_display(user):
    try:
        profile = user.profile
    except models.Profile.DoesNotExist:
        return user.email
    return profile.get_full_name()


def get_admin_email():
    env = environ.Env()
    return list(env.dict("ADMINS").values())[0]


class ExportCsvMixin:
    def export_csv(self, request, queryset, model, filename):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(filename)
        writer = csv.writer(response)

        field_names = model.get_exportable_field_names()
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow(obj.convert_to_row(field_names))

        return response

    export_csv.short_description = "Export as CSV"

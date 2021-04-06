from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from eahub.feedback.models import Feedback


class FeedbackResource(ModelResource):
    class Meta:
        model = Feedback
        export_order = ["id", "creation_time", "email", "message", "page_url"]


@admin.register(Feedback)
class FeedbackAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("creation_time", "email", "message", "page_url")
    search_fields = ["email", "message"]
    list_filter = ["creation_time", "email"]
    ordering = ["-creation_time"]
    resource_class = FeedbackResource

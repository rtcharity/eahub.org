from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from .models import Feedback

class FeedbackResource(ModelResource):
    class Meta:
        model = Feedback
        export_order = ["id", "creation_time", "email", "message", "page_url"]

class FeedbackAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = (
        "creation_time",
        "email",
        "message", 
    )
    search_fields = ["email", "message"]
    ordering = ["-creation_time"]
    resource_class = FeedbackResource

admin.site.register(Feedback, FeedbackAdmin)

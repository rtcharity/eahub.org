from django.urls import include, path

from . import views

app_name = "profiles_app"

urlpatterns = [
    path("", views.my_profile, name="my_profile"),
    path("edit/", views.ProfileUpdate.as_view(), name="edit_profile"),
    path(
        "import-confirmation/",
        views.ProfileUpdateImport.as_view(),
        name="profile_update_import",
    ),
    path("delete/", views.delete_profile, name="delete_profile"),
    path(
        "<int:legacy_record>/",
        views.profile_redirect_from_legacy_record,
        name="profile_legacy",
    ),
    path("<slug:slug>/", views.profile_detail_or_redirect, name="profile"),
    path(
        "<slug:slug>/report-abuse/",
        views.ReportProfileAbuseView.as_view(),
        name="report_abuse_profile",
    ),
    path(
        "<slug:slug>/message/",
        views.SendProfileMessageView.as_view(),
        name="message_profile",
    ),
    path("api/", include("eahub.profiles.api.urls", namespace="api")),
]

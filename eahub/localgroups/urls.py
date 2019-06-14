from django import urls

from . import views


urlpatterns = [
    urls.path("new/", views.LocalGroupCreateView.as_view(), name="localgroups_create"),
    urls.path("<slug:slug>/claim/", views.claim_group, name="claim_group"),
    urls.path(
        "<slug:slug>/report-inactive/",
        views.report_group_inactive,
        name="report_group_inactive",
    ),
    urls.path("<slug:slug>/", views.LocalGroupDetailView.as_view(), name="group"),
    urls.path(
        "<slug:slug>/edit/",
        views.LocalGroupUpdateView.as_view(),
        name="localgroups_update",
    ),
    urls.path(
        "<slug:slug>/delete/",
        views.LocalGroupDeleteView.as_view(),
        name="localgroups_delete",
    ),
    urls.path(
        "<slug:slug>/report-abuse/",
        views.ReportGroupAbuseView.as_view(),
        name="report_abuse_group",
    ),
]

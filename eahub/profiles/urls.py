from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.MyProfileView, name='my_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('edit/cause_areas/', views.edit_profile_cause_areas, name='edit_profile_cause_areas'),
    path('edit/career/', views.edit_profile_career, name='edit_profile_career'),
    path('edit/community/', views.edit_profile_community, name='edit_profile_community'),
    path('delete/', views.delete_profile, name='delete_profile'),
    path('download/', views.DownloadView, name='download_profile'),
    path('<int:legacy_record>/', views.profile_redirect_from_legacy_record, name='profile_legacy'),
    path('<slug:slug>/', views.profile_detail_or_redirect, name='profile'),
    path(
        '<slug:slug>/report-abuse/',
        views.report_abuse,
        name='report_abuse_profile'
    ),
    path(
        '<slug:slug>/report-abuse-done/',
        TemplateView.as_view(template_name='eahub/report_abuse_done.html'),
        name='report_abuse_profile_done'
    ),
]

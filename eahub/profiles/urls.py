from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyProfileView, name='my_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('edit/cause_areas/', views.edit_profile_cause_areas, name='edit_profile_cause_areas'),
    path('edit/career/', views.edit_profile_career, name='edit_profile_career'),
    path('edit/community/', views.edit_profile_community, name='edit_profile_community'),
    path('delete/', views.delete_profile, name='delete_profile'),
    path('download/', views.DownloadView, name='download_profile'),
    path('<slug:slug>/', views.ProfileDetailView.as_view(), name='profile'),
]

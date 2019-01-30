from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyProfileView, name='my_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:profile_id>', views.ProfileView, name='profile'),
    path('edit', views.edit_profile, name='edit_profile'),
    path('delete', views.delete_profile, name='delete_profile'),
]

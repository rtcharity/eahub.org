from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<int:profile_id>', views.ProfileView, name='profile'),
    path('my_profile', views.MyProfileView, name='my_profile'),
]

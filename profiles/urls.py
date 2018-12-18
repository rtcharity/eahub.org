from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('my_profile/', views.ProfileView, name='my_profile'),
]
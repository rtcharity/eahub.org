from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.profiles, name='profiles'),
    path('groups/', views.groups, name='groups'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls, name='admin'),
]
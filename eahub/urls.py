from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('', views.index, name='index'),
    path('profiles/', views.profiles, name='profiles'),
    path('groups/', views.groups, name='groups'),
    path('profile/', include('profiles.urls')),
    path('profile/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls, name='admin'),
]
from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include('profiles.urls')),
    path('profile/', include('django.contrib.auth.urls')),
    path('profiles', views.profiles, name='profiles'),
    path('group/', include('groups.urls')),
    path('groups/', views.groups, name='groups'),
    path('admin/', admin.site.urls, name='admin'),
    path('about/', views.about, name='about')
]

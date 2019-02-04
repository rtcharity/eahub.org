from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from . import views

admin.site.site_header = settings.ADMIN_SITE_HEADER

handler403 = views.forbidden
handler404 = views.not_found
handler500 = views.server_error

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include('profiles.urls')),
    path('profile/', include('django.contrib.auth.urls')),
    path('profiles', views.profiles, name='profiles'),
    path('group/', include('groups.urls')),
    path('groups/', views.groups, name='groups'),
    path('admin/', admin.site.urls, name='admin'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacyPolicy, name='privacyPolicy')
]

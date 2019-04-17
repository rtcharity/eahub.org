from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from ..base import views

admin.site.login = login_required(admin.site.login)
admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/password/change/', views.CustomisedPasswordChangeView.as_view(), name='account_reset_password'),
    url('accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$', views.CustomisedPasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('eahub.profiles.urls')),
    path('profiles/', views.profiles, name='profiles'),
    path('group/', include('eahub.localgroups.urls')),
    path('groups/', views.groups, name='groups'),
    path('admin/', admin.site.urls, name='admin'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacyPolicy, name='privacyPolicy'),
    path('favicon.ico', views.FaviconView.as_view(), name='favicon'),
    path('robots933456.txt', views.healthCheck, name='healthCheck'),
    path('trigger-500-error/', views.trigger500Error, name='trigger500Error'),
]

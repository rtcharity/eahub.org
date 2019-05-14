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
    path('about/newsletter/', TemplateView.as_view(template_name='eahub/newsletter.html'), name='newsletter'),
    path('privacy-policy/', views.privacyPolicy, name='privacyPolicy'),
    path('favicon.ico', views.FaviconView.as_view(), name='favicon'),
    path('robots.txt', views.RobotsTxtView.as_view(), name='robots.txt'),
    path('robots933456.txt', views.healthCheck, name='healthCheck'),

    # Redirects from legacy URLs
    path('actions/', views.LegacyRedirectView.as_view(url='https://www.effectivealtruism.org/get-involved/')),
    path('actions/donating/', views.LegacyRedirectView.as_view(url='https://donationswap.eahub.org/charities')),
    path('contact/', views.LegacyRedirectView.as_view(url='https://resources.eahub.org/contact-lean/')),
    path('eahub.org/groups/resources/recruiting-managing-members/', views.LegacyRedirectView.as_view(url='https://resources.eahub.org/guides_and_tips/tips-from-local-organisers/')),
    path('groups/facebook-invites/', views.LegacyRedirectView.as_view(url='https://stackoverflow.com/questions/27080936/how-can-i-select-all-friends-in-new-facebook-events-invite-ui#33698935')),
    path('groups/get-a-website/', views.LegacyRedirectView.as_view(url='https://github.com/rtcharity/lean-site-template')),
    path('groups/local-group-support-overview-lean-cea-and-eaf/', views.LegacyRedirectView.as_view(url='https://forum.effectivealtruism.org/posts/Cvi7hnTYMk5qutkDg/local-effective-altruism-network-s-new-focus-for-2019')),
    path('groups/resources/giving-games/', views.LegacyRedirectView.as_view(url='https://docs.google.com/document/d/1g5G0PvYFs7cAbAZ8ANI_wnsv7DjtBmq4_SQcg44-HDA/edit')),
    path('index.php/', views.LegacyRedirectView.as_view(pattern_name='index')),
    path('links/', views.LegacyRedirectView.as_view(url='https://resources.eahub.org (temporarily)')),
    path('map/', views.LegacyRedirectView.as_view(pattern_name='profiles')),
    path('map/people/all/', views.LegacyRedirectView.as_view(pattern_name='profiles')),
    path('profile/login/', views.LegacyRedirectView.as_view(pattern_name='account_login')),
    path('profile/signup/', views.LegacyRedirectView.as_view(pattern_name='account_signup')),
    path('register/', views.LegacyRedirectView.as_view(pattern_name='account_signup')),
    path('user/', views.LegacyRedirectView.as_view(pattern_name='my_profile')),
    path('user/<int:legacy_record>/', views.LegacyRedirectView.as_view(pattern_name='profile_legacy')),
    path('user/<slug:slug>/', views.LegacyRedirectView.as_view(pattern_name='profile')),
    path('user/profiles/', views.LegacyRedirectView.as_view(pattern_name='profiles')),
    path('user/profiles/offers', views.LegacyRedirectView.as_view(pattern_name='profiles')),
    path('user.php/', views.LegacyRedirectView.as_view(pattern_name='my_profile')),
    path('wp-login.php/', views.LegacyRedirectView.as_view(pattern_name='account_login')),
]

handler404 = "eahub.base.views.page_not_found"

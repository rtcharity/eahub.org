from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sitemaps.views import sitemap
from django.http import Http404
from django.urls import include, path
from django.views.generic import TemplateView

from ..base import views
from ..profiles.models import Profile
from ..profiles.sitemap import ProfilesSitemap
from ..profiles.views import profiles


def staff_or_404(u):
    if u.is_active:
        if u.is_staff:
            return True
        raise Http404()
    return False


admin.site.login = user_passes_test(staff_or_404)(admin.site.login)

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path("", views.HomepageView.as_view(), name="index"),
    path("homepage-map/", views.HomepageMapView.as_view(), name="homepage_map"),
    path(
        "accounts/password/change/",
        views.CustomisedPasswordChangeView.as_view(),
        name="account_reset_password",
    ),
    url(
        "accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.CustomisedPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("eahub.profiles.urls")),
    path("profiles/", profiles, name="profiles"),
    path("candidates/", views.candidates, name="candidates"),
    path("speakers/", views.speakers, name="speakers"),
    path("volunteers/", views.volunteers, name="volunteers"),
    path("group/", include("eahub.localgroups.urls")),
    path("groups/", views.groups, name="groups"),
    path("admin/", admin.site.urls, name="admin"),
    path("about/", views.about, name="about"),
    path(
        "newsletter/",
        TemplateView.as_view(template_name="eahub/newsletter.html"),
        name="newsletter",
    ),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("robots.txt", views.RobotsTxtView.as_view(), name="robots.txt"),
    path("robots933456.txt", views.health_check, name="health_check"),
    path("ads.txt", views.AdsTxtView.as_view(), name="ads.txt"),
    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": {
                "profiles": ProfilesSitemap({"queryset": Profile.objects.all()})
            }
        },
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

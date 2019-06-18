from allauth.account import app_settings, utils
from allauth.account.views import PasswordChangeView, PasswordResetFromKeyView
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.templatetags import static
from django.urls import reverse, reverse_lazy
from django.views.generic import base
from django.views.generic.edit import FormView

from ..localgroups.models import LocalGroup as Group
from ..profiles.models import Profile
from .forms import ReportAbuseForm


class CustomisedPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "account/password_reset_from_key.html"

    def form_valid(self, form):
        super().form_valid(form)
        return utils.perform_login(
            self.request,
            self.reset_user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=reverse("edit_profile"),
        )


class CustomisedPasswordChangeView(PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy("my_profile")


def index(request):
    groups_data = get_groups_data()
    profiles_data = get_profiles_data(request.user)
    private_profiles = get_private_profiles(request.user)
    return render(
        request,
        "eahub/index.html",
        {
            "page_name": "Home",
            "groups": groups_data["rows"],
            "profiles": profiles_data["rows"],
            "map_locations": {
                "profiles": profiles_data["map_data"],
                "groups": groups_data["map_data"],
                "private_profiles": private_profiles,
            },
        },
    )


def about(request):
    return render(request, "eahub/about.html")


def privacy_policy(request):
    return render(request, "eahub/privacy_policy.html")


def profiles(request):
    profiles_data = get_profiles_data(request.user)
    private_profiles = get_private_profiles(request.user)
    return render(
        request,
        "eahub/profiles.html",
        {
            "page_name": "Profiles",
            "profiles": profiles_data["rows"],
            "map_locations": {
                "profiles": profiles_data["map_data"],
                "private_profiles": private_profiles,
            },
        },
    )


def groups(request):
    groups_data = get_groups_data()
    return render(
        request,
        "eahub/groups.html",
        {
            "page_name": "Groups",
            "groups": groups_data["rows"],
            "map_locations": {"profiles": groups_data["map_data"]},
        },
    )


def get_groups_data():
    rows = Group.objects.all()
    map_data = [
        {
            "lat": x.lat,
            "lng": x.lon,
            "label": x.name,
            "active": x.is_active,
            "path": f"/group/{x.slug}",
        }
        for x in rows
        if x.lat and x.lon
    ]
    return {"rows": rows, "map_data": map_data}


def get_profiles_data(user):
    rows = Profile.objects.visible_to_user(user)
    map_data = [
        {"lat": x.lat, "lng": x.lon, "label": x.name, "path": f"/profile/{x.slug}"}
        for x in rows
        if x.lat and x.lon
    ]
    return {"rows": rows, "map_data": map_data}


def get_private_profiles(user):
    k_anonymity = 15
    private_profiles = (
        Profile.objects.filter(is_public=False, lat__isnull=False, lon__isnull=False)
        .exclude(user_id=user.id)
        .values("lat", "lon")
        .annotate(count=Count("*"))
        .filter(count__gte=k_anonymity)
        .order_by()
    )
    private_profiles_json = [
        {"lat": x["lat"], "lng": x["lon"], "count": x["count"]}
        for x in private_profiles
    ]
    return private_profiles_json


class FaviconView(base.RedirectView):
    def get_redirect_url(self):
        return static.static("favicon.ico")


class LegacyRedirectView(base.RedirectView):
    permanent = True


class RobotsTxtView(base.TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain; charset=utf-8"


class AdsTxtView(base.TemplateView):
    template_name = "ads.txt"
    content_type = "text/plain; charset=utf-8"


class ReportAbuseView(FormView):
    template_name = "eahub/report_abuse.html"
    form_class = ReportAbuseForm

    def form_valid(self, form):
        reasons = form.cleaned_data
        reportee = self.profile()
        type = self.get_type()
        subject = f"EA {type} reported as abuse: {reportee.name}"
        message = render_to_string(
            "emails/report_{}_abuse.txt".format(type),
            {
                "profile_name": reportee.name,
                "profile_url": "https://{0}/profile/{1}".format(
                    get_current_site(self.request).domain, reportee.slug
                ),
                "reasons": ", ".join(reasons),
            },
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.LEAN_MANAGERS,
        )
        messages.success(
            self.request,
            "Thank you, we have received your report. "
            "Our admin team will send you an email once they have looked into it.",
        )
        return redirect("/{0}/{1}".format(type, reportee.slug))


def health_check(request):
    return HttpResponse(status=204)

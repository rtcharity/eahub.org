from django.core import mail
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.templatetags import static
from django.views import defaults
from django.views.generic import base
from allauth.account import app_settings
from allauth.account import utils
from allauth.account.views import SignupView, LoginView, PasswordResetView, PasswordResetFromKeyView, PasswordChangeView, EmailView
from django.urls import reverse, reverse_lazy

from . import exceptions
from ..localgroups.models import LocalGroup as Group
from ..profiles.models import Profile
from django.db.models import Count

class CustomisedPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = 'account/password_reset_from_key.html'

    def form_valid(self, form):
        super().form_valid(form)
        return utils.perform_login(
            self.request,
            self.reset_user,
            email_verification=app_settings.EMAIL_VERIFICATION,
            redirect_url=reverse("edit_profile"),
        )


class CustomisedPasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy("my_profile")


def index(request):
    groupsData = getGroupsData()
    profilesData = getProfilesData(request.user)
    privateProfiles = getPrivateProfiles(request.user)
    return render(request, 'eahub/index.html', {
        "page_name": "Home",
        'groups': groupsData["rows"],
        'profiles': profilesData["rows"],
        "map_locations": {
            "profiles": profilesData["map_data"],
            "groups": groupsData["map_data"],
            "private_profiles": privateProfiles,
        }
    })

def about(request):
    return render(request, 'eahub/about.html')

def privacyPolicy(request):
    return render(request, 'eahub/privacy_policy.html')

def profiles(request):
    profilesData = getProfilesData(request.user)
    privateProfiles = getPrivateProfiles(request.user)
    return render(request, 'eahub/profiles.html', {
        'page_name': 'Profiles',
        'profiles': profilesData["rows"],
        'map_data_profiles': profilesData["map_data"],
        'private_profiles': privateProfiles
    })

def groups(request):
    groupsData = getGroupsData()
    return render(request, 'eahub/groups.html', {
        'page_name': 'Groups',
        'groups': groupsData["rows"],
        'map_data_groups': groupsData["map_data"]
    })

def getGroupsData():
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
    return {
        'rows': rows,
        'map_data': map_data
    }

def getProfilesData(user):
    rows = Profile.objects.visible_to_user(user)
    map_data = [
        {
            "lat": x.lat,
            "lng": x.lon,
            "label": x.name,
            "path": f"/profile/{x.slug}",
        }
        for x in rows
        if x.lat and x.lon
    ]
    return {
        'rows': rows,
        'map_data': map_data
    }

def getPrivateProfiles(user):
    kAnonymity = 15
    privateProfiles = Profile.objects.filter(is_public=False, lat__isnull=False, lon__isnull=False).exclude(user_id=user.id).values('lat', 'lon').annotate(count=Count('*')).filter(count__gte=kAnonymity).order_by()
    private_profiles_json = [
        {"lat": x["lat"], "lng": x["lon"], "count": x["count"]}
        for x in privateProfiles
    ]
    return private_profiles_json


class FaviconView(base.RedirectView):
    def get_redirect_url(self):
        return static.static("favicon.ico")


def healthCheck(request):
    return HttpResponse(status=204)

def trigger500Error(request):
    raise RuntimeError("Test error, safe to ignore")


def page_not_found(request, exception):
    if not isinstance(exception, exceptions.Quiet404):
        mail.mail_managers(
            "Broken link",
            loader.render_to_string("emails/broken_link.txt", {"request": request}),
        )
    return defaults.page_not_found(request, exception)

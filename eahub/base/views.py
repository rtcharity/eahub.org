from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from ..localgroups.models import LocalGroup as Group
from ..profiles.models import Profile

def index(request):
    groupsData = getGroupsData()
    profilesData = getProfilesData()
    return render(request, 'eahub/index.html', {
        "page_name": "Home",
        'groups': groupsData["rows"],
        'map_data_groups': groupsData["map_data"],
        'profiles': profilesData["rows"],
        'map_data_profiles': profilesData["map_data"]
    })

def about(request):
    return render(request, 'eahub/about.html')

def privacyPolicy(request):
    return render(request, 'eahub/privacy_policy.html')

def profiles(request):
    profilesData = getProfilesData()
    return render(request, 'eahub/profiles.html', {
        'page_name': 'Profiles',
        'profiles': profilesData["rows"],
        'map_data_profiles': profilesData["map_data"]
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
    map_data = ''.join([
        '{' +
            'lat: {lat}, lng: {lon}, label:"{name}", active:"{active}", path: "{path}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=x.name,
                active=x.is_active,
                path='/{obj}/{slug}'.format(
                    obj='group',
                    slug=x.slug
                )
            )
        + '},'
        for x in rows
        if x.lat and x.lon
    ])
    return {
        'rows': rows,
        'map_data': map_data
    }

def getProfilesData():
    rows = Profile.objects.all()
    map_data = ''.join([
        '{' +
            'lat: {lat}, lng: {lon}, label:"{name}", path: "{path}", gdpr_confirmed: "{gdpr_confirmed}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=x.name,
                path='/{obj}/{slug}'.format(
                    obj='profile',
                    slug=x.slug
                ),
                gdpr_confirmed=True
            )
        + '},'
        for x in rows
        if x.lat and x.lon
    ])
    return {
        'rows': rows,
        'map_data': map_data
    }

def healthCheck(request):
    return HttpResponse(status=204)

def trigger500Error(request):
    raise RuntimeError("Test error, safe to ignore")

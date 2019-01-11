from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from groups.models import Group
from profiles.models import Profile

def index(request):
    return render(request, 'eahub/index.html', {
        "page_name": "Home"
    })

def profiles(request):
    groupsData = getGroupsData()
    profilesData = getProfilesData()
    return render(request, 'eahub/profiles.html', {
        'page_name': 'Profiles',
        'profiles': profilesData["rows"],
        'map_data_groups': groupsData["map_data"],
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
            'lat: {lat}, lng: {lon}, label:"{name}", path: "{path}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=x.name,
                path='/{obj}/{id}'.format(
                    obj='group',
                    id=x.id
                )
            )
        + '},'
        for x in rows
        if x.lat
    ])
    return {
        'rows': rows,
        'map_data': map_data
    }

def getProfilesData():
    rows = Profile.objects.all()
    map_data = ''.join([
        '{' +
            'lat: {lat}, lng: {lon}, label:"{name}", path: "{path}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=' '.join([x.first_name, x.last_name]),
                path='/{obj}/{id}'.format(
                    obj='profile',
                    id=x.id
                )
            )
        + '},'
        for x in rows
        if x.lat
    ])
    return {
        'rows': rows,
        'map_data': map_data
    }

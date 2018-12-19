from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from groups.models import Group
from profiles.models import Profile

def index(request):
    rows = Group.objects\
        .exclude(lat__isnull=True)
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
    ])
    return render(request, 'eahub/index.html', {
        'map_data': map_data
    })

def profiles(request):
    rows_groups = Group.objects\
        .exclude(lat__isnull=True)
    map_data_groups = ''.join([
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
        for x in rows_groups
    ])
    rows_profiles = Profile.objects\
        .exclude(lat__isnull=True)
    map_data_profiles = ''.join([
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
        for x in rows_profiles
    ])
    return render(request, 'eahub/profiles.html', {
        'page_name': 'Profiles',
        'profiles': rows_profiles,
        'map_data_groups': map_data_groups,
        'map_data_profiles': map_data_profiles
    })

def groups(request):
    rows_groups = Group.objects\
        .exclude(lat__isnull=True)
    map_data_groups = ''.join([
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
        for x in rows_groups
    ])
    rows_profiles = Profile.objects\
        .exclude(lat__isnull=True)
    map_data_profiles = ''.join([
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
        for x in rows_profiles
    ])
    return render(request, 'eahub/groups.html', {
        'page_name': 'Groups',
        'groups': rows_groups,
        'map_data_groups': map_data_groups,
        'map_data_profiles': map_data_profiles
    })

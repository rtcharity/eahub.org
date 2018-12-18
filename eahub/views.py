from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from groups.models import Group
from profiles.models import Profile

def index(request):
    rows = Group.objects\
        .exclude(lat__isnull=True)\
        .order_by('country', 'city_or_town', 'name')
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
    rows = Profile.objects\
        .exclude(lat__isnull=True)\
        .order_by('country', 'city_or_town', 'first_name', 'last_name')
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
    ])    
    return render(request, 'eahub/profiles.html', {
        'page_name': 'Profiles',
        'profiles': rows,
        'map_data': map_data
    })

def groups(request):
    rows = Group.objects\
        .exclude(lat__isnull=True)\
        .order_by('country', 'city_or_town', 'name')
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
    return render(request, 'eahub/groups.html', {
        'page_name': 'Groups',
        'groups': rows,
        'map_data': map_data
    })
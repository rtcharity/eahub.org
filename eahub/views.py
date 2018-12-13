from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from .models import Group
from users.models import Profile

def index(request):
    return render(request, 'eahub/index.html', {
        
    })

def profiles(request):
    rows = Profile.objects\
        .exclude(lat__isnull=True)
    rows = Paginator(rows, 100).get_page(1) # remove when caching is implemented
    map_data = ''.join([
        '{' +
            'lat: {lat}, lng: {lon}, label:"{name}", link: "{link}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=' '.join([x.user.first_name, x.user.last_name]),
                link='/{obj}/{id}'.format(
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
            'lat: {lat}, lng: {lon}, label:"{name}", link: "{link}"'.format(
                lat=str(x.lat),
                lon=str(x.lon),
                name=x.name,
                link='/{obj}/{id}'.format(
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
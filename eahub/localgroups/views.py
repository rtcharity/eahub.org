import json
from datetime import datetime 

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import LocalGroup as Group

def view_group(request, slug):
    group = Group.objects.get(slug=slug)
    return render(request, 'eahub/group.html', {
        'group': group
    })

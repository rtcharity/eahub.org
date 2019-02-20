import json
from datetime import datetime 

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import LocalGroup as Group

def view_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    return render(request, 'eahub/group.html', {
        'group': group
    })

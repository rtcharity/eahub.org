from django.shortcuts import render

from .models import Group

def GroupView(request, group_id):
    row = Group.objects\
        .filter(id=group_id)\
        .first()
    return render(request, 'eahub/group.html', {
        'group': row
    })

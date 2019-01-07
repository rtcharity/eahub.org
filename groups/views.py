from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Group
from .forms import GroupCreationForm

def view_group(request, group_id):
    row = Group.objects\
        .filter(id=group_id)\
        .first()
    return render(request, 'eahub/group.html', {
        'group': row
    })

def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group', group_id=group.id)
    else:
        form = GroupCreationForm()
    return render(request, 'eahub/create_group.html', {'form': form})
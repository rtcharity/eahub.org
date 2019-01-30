import json
from datetime import datetime 

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Group
from .forms import CreateGroupForm, EditGroupForm

def view_group(request, group_id):
    row = Group.objects\
        .filter(id=group_id)\
        .first()
    return render(request, 'eahub/group.html', {
        'group': row
    })

@login_required(login_url=reverse_lazy('login'))
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group = group.geocode()
            group.save()
            group.organisers.add(request.user)
            return redirect('group', group_id=group.id)
    else:
        form = CreateGroupForm()
    return render(request, 'eahub/edit_group.html', {
        'form': form
    })

@login_required(login_url=reverse_lazy('login'))
def edit_group(request, group_id):
    group = Group.objects\
        .filter(id=group_id, organisers__in=[request.user])\
        .first()
    assert group, 'User {} cannot edit Group {}'.format(
        request.user.id, group_id
    )
    if request.method == 'POST':
        form = EditGroupForm(request.POST, instance=group)
        if form.is_valid():
            if form.changed_data:
                group = form.save(commit=False)
                group = group.geocode()
                group.save()
                # update edit_history on Group as groups can be edited by lots
                # of different people, we should keep a log of all changes
                orginal_object = Group.objects.get(pk=group_id)
                diff = {
                    key: {
                        'before': orginal_object.__dict__[key],
                        'after': value
                    }
                    for key, value in form.cleaned_data.items()
                    if key in form.changed_data
                }
                edit_history = orginal_object.get_edit_history()
                edit_history.append({
                    'date': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
                    'user': {'id': request.user.id, 'email': request.user.email},
                    'diff': {key: str(value) for key, value in diff.items()}
                })
                orginal_object.edit_history = json.dumps(edit_history)
                orginal_object.save()
            return redirect('group', group_id=group_id)
    else:        
        form = EditGroupForm(instance=group)
        return render(request, 'eahub/edit_group.html', {
            'form': form
        })
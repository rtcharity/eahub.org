import os

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import requests

from .models import Profile
from .forms import ProfileCreationForm, EditProfileForm


def recaptcha_valid(recaptcha_response):
    request = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        {
            'secret': os.environ['RECAPTCHA_PRIVATE_KEY'],
            'response': recaptcha_response
        }
    ).json()
    return request.get('success', False)


class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'    
    form_class = ProfileCreationForm
    success_url = reverse_lazy('my_profile')
    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        if recaptcha_valid(self.request.POST.get('g-recaptcha-response')):
            login(self.request, new_user)
        else:
            new_user.delete() # delete recaptcha failing user made by robot
        return valid


def ProfileView(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    return render(request, 'eahub/profile.html', {
        'profile': profile
    })


@login_required(login_url=reverse_lazy('login'))
def MyProfileView(request):
    return redirect('profile', profile_id=request.user.id)


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'eahub/edit_profile.html', {
            'form': form
        })
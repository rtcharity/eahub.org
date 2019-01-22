import os

import requests
from django.conf import settings
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileCreationForm, EditProfileForm


class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'    
    form_class = ProfileCreationForm
    success_url = reverse_lazy('my_profile')
    extra_context = {'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY}
    def form_valid(self, form):
        recaptcha_valid = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': self.request.POST.get('g-recaptcha-response')
            }
        ).json().get('success', False)
        if recaptcha_valid:
            # log user in
            valid = super(SignUp, self).form_valid(form)
            email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
            new_user = authenticate(email=email, password=password)
            login(self.request, new_user)
            return valid
        else:
            # fail
            return redirect(reverse('signup') + '?captcha_error=True')       


def ProfileView(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    template = 'eahub/profile.html'
    if not profile.gdpr_confirmed: template = 'eahub/profile_locked.html'
    return render(request, template, {
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
            profile = form.save(commit=False)
            profile.gdpr_confirmed = True
            profile = profile.geocode()
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'eahub/edit_profile.html', {
            'form': form
        })

import os, logging

import requests
from django.conf import settings
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import *


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
def DownloadView(request):
    profile = Profile.objects.get(pk=request.user.id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_profile.csv"'
    return profile.csv(response)


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.gdpr_confirmed = True
            profile = profile.geocode()
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'eahub/edit_profile.html', {
            'form': form,
            'profile': profile
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_cause_areas(request):
    if request.method == 'POST':
        form = EditProfileCauseAreasForm(request.POST, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            cause_areas = request.POST.getlist('custom_cause_areas')
            profile.cause_areas = cause_areas
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileCauseAreasForm(instance=request.user)
        return render(request, 'eahub/edit_profile_cause_areas.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.id)
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_career(request):
    if request.method == 'POST':
        form = EditProfileCareerForm(request.POST, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            expertise = request.POST.getlist('custom_expertise')
            profile.expertise = expertise
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileCareerForm(instance=request.user)
        return render(request, 'eahub/edit_profile_career.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.id)
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_community(request):
    if request.method == 'POST':
        form = EditProfileCommunityForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = EditProfileCommunityForm(instance=request.user)
        return render(request, 'eahub/edit_profile_community.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.id)
        })


@login_required(login_url=reverse_lazy('login'))
def delete_profile(request):
    if request.method == 'POST':
        logging.info('user_id={} full_name={} has deleted their account'.format(
            request.user.id,
            request.user.full_name()
        ))
        profile = Profile.objects.get(
            id=request.user.id
        )
        profile.delete()
        return redirect('logout')
    else:
        form = DeleteProfileForm()
        return render(request, 'eahub/delete_profile.html', {
            'form': form
        })

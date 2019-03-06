import os, logging

import requests
from django.conf import settings
from django.views import generic
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CauseArea, ExpertiseArea, GivingPledge, Profile, OrganisationalAffiliation, Membership
from ..localgroups.models import LocalGroup
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


def ProfileView(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    template = 'eahub/profile.html'
    return render(request, template, {
        'profile': profile
    })


@login_required(login_url=reverse_lazy('login'))
def MyProfileView(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    return redirect('profile', slug=request.user.profile.slug)


@login_required(login_url=reverse_lazy('login'))
def DownloadView(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    profile = Profile.objects.get(pk=request.user.profile.id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_profile.csv"'
    return profile.csv(response)


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    profile = Profile.objects.get(pk=request.user.profile.id)
    if request.method == 'POST':
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile = profile.geocode()
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'eahub/edit_profile.html', {
            'form': form,
            'profile': profile
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_cause_areas(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    if request.method == 'POST':
        form = EditProfileCauseAreasForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            cause_areas = request.POST.getlist('cause_areas')
            profile.cause_areas = cause_areas
            giving_pledges = request.POST.getlist('giving_pledges')
            profile.giving_pledges = giving_pledges
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileCauseAreasForm(instance=request.user.profile)
    return render(request, 'eahub/edit_profile_cause_areas.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.profile.id),
            'cause_area_choices': CauseArea.choices,
            'giving_pledge_choices': GivingPledge.choices,
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_career(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    if request.method == 'POST':
        form = EditProfileCareerForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            expertise_areas = request.POST.getlist('expertise_areas')
            profile.expertise_areas = expertise_areas
            profile.save()
            return redirect('my_profile')
    else:
        form = EditProfileCareerForm(instance=request.user.profile)
    return render(request, 'eahub/edit_profile_career.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.profile.id),
            'expertise_area_choices': ExpertiseArea.choices,
        })


@login_required(login_url=reverse_lazy('login'))
def edit_profile_community(request):
    if not hasattr(request.user, 'profile'):
        raise http.Http404("user has no profile")
    if request.method == 'POST':
        form = EditProfileCommunityForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.local_groups.clear()
            organisational_affiliations = request.POST.getlist('organisational_affiliations')
            profile.organisational_affiliations = organisational_affiliations
            group_affiliations = request.POST.getlist('local_groups')
            local_groups = LocalGroup.objects.filter(id__in=group_affiliations)
            for group in local_groups:
                membership = Membership(profile=profile, local_group=group)
                membership.save()
            return redirect('my_profile')
    else:
        form = EditProfileCommunityForm(instance=request.user.profile)
    return render(request, 'eahub/edit_profile_community.html', {
            'form': form,
            'profile': Profile.objects.get(pk=request.user.profile.id),
            'organisational_affiliation_choices': OrganisationalAffiliation.choices,
        })


@login_required(login_url=reverse_lazy('login'))
def delete_profile(request):
    if request.method == 'POST':
        logging.info('user_id={} email={} has deleted their account'.format(
            request.user.id,
            request.user.email
        ))
        user = User.objects.get(
            id=request.user.id
        )
        user.delete()
        return redirect('logout')
    else:
        form = DeleteProfileForm()
        return render(request, 'eahub/delete_profile.html', {
            'form': form
        })

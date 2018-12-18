import os

from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import requests

from .models import Profile
from .forms import ProfileCreationForm


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
    row = Profile.objects\
        .filter(id=profile_id)\
        .first()
    return render(request, 'eahub/profile.html', {
        'profile': row
    })


@login_required(login_url=reverse_lazy('login'))
def MyProfileView(request):
    return render(request, 'eahub/my_profile.html', {
        'user': request.user
    })
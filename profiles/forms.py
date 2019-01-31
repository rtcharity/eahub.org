from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class ProfileChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = UserChangeForm.Meta.fields


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name',
            'image', 'summary',
            'city_or_town', 'country',            
        )

class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

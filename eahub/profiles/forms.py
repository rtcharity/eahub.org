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


class EditProfileCauseAreasForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            # 'cause_areas' is set using custom code in view
            'cause_areas_other',
            'giving_pledge', 'giving_pledge_other',
            'available_to_volunteer',           
        )


class EditProfileCareerForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            # 'expertise' is set using custom code in view
            'open_to_job_offers',
            'expertise_other',           
        )


class EditProfileCommunityForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = (
            'available_as_speaker',
            'topics_i_speak_about',    
        )


class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

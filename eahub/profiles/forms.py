from authtools.forms import CaseInsensitiveUsernameFieldCreationForm
from django import forms
from django.db import models
from .models import Profile, CauseArea, GivingPledge
from ..base.models import User

class ProfileCreationForm(CaseInsensitiveUsernameFieldCreationForm):

    name = forms.CharField(max_length=200)
    subscribed_to_email_updates = forms.BooleanField()

    def save(self, commit=True):
        if not commit:
            raise RuntimeError("can't create profile without database save")
        name = self.cleaned_data['name']
        subscribed_to_email_updates = self.cleaned_data['subscribed_to_email_updates']
        user = super().save()
        Profile.objects.create(user=user, name=name, subscribed_to_email_updates=subscribed_to_email_updates)
        return user

    class Meta(CaseInsensitiveUsernameFieldCreationForm.Meta):
        model = User
        fields = ['email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'image', 'summary',
            'city_or_town', 'country',
            'subscribed_to_email_updates',
        )


class EditProfileCauseAreasForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'available_to_volunteer',           
        )


class EditProfileCareerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'open_to_job_offers',
        )


class EditProfileCommunityForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'available_as_speaker',
        )


class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

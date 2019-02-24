from authtools.forms import CaseInsensitiveUsernameFieldCreationForm
from django import forms
from django.db import models
from .models import Profile, CauseArea, GivingPledge
from ..base.models import User

class ProfileCreationForm(CaseInsensitiveUsernameFieldCreationForm):

    name = forms.CharField(max_length=200)
    subscribed_to_email_updates = forms.BooleanField(required=False)

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
        widgets = {
            'city_or_town': forms.TextInput(attrs={'placeholder': 'London'}),
            'country': forms.TextInput(attrs={'placeholder': 'UK'}),
            'summary': forms.Textarea(attrs={'rows': 7, 'placeholder': "In West Philadelphia born and raised. On the playground is where I spent most of my days."}),
        }
        labels = {
            'city_or_town': ('City/Town'),
            'subscribed_to_email_updates': ('Send me email updates about the EA Hub'),
        }


class EditProfileCauseAreasForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'available_to_volunteer',
        )
        labels = {
            'available_to_volunteer': ('Available to volunteer:')
        }


class EditProfileCareerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'open_to_job_offers',
        )
        labels = {
            'open_to_job_offers': ('Open to job offers:')
        }


class EditProfileCommunityForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'available_as_speaker',
        )
        labels = {
            'available_as_speaker': ('Available as speaker:')
        }

class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

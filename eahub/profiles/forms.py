from authtools.forms import CaseInsensitiveUsernameFieldCreationForm
from django import forms
from django.db import models
from .models import Profile, CauseArea, GivingPledge
from ..localgroups.models import LocalGroup
from ..base.models import User

class CustomisedModelMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return "%s" % (obj.name)

class ProfileCreationForm(CaseInsensitiveUsernameFieldCreationForm):

    name = forms.CharField(max_length=200)
    is_public = forms.BooleanField(required=False, label="Show my profile to the public", initial=True)
    subscribed_to_email_updates = forms.BooleanField(required=False, label='Send me email updates about the EA Hub')

    def save(self, commit=True):
        if not commit:
            raise RuntimeError("can't create profile without database save")
        is_public = self.cleaned_data['is_public']
        name = self.cleaned_data['name']
        subscribed_to_email_updates = self.cleaned_data['subscribed_to_email_updates']
        user = super().save()
        Profile.objects.create(user=user, is_public=is_public, name=name, subscribed_to_email_updates=subscribed_to_email_updates)
        return user

    class Meta(CaseInsensitiveUsernameFieldCreationForm.Meta):
        model = User
        fields = ['name', 'email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'name',
            'image', 'summary',
            'city_or_town', 'country',
            'is_public',
            'subscribed_to_email_updates',
        )
        widgets = {
            'city_or_town': forms.TextInput(attrs={'placeholder': 'London'}),
            'country': forms.TextInput(attrs={'placeholder': 'UK'}),
            'summary': forms.Textarea(attrs={'rows': 7, 'placeholder': "In West Philadelphia born and raised. On the playground is where I spent most of my days."}),
        }
        labels = {
            'city_or_town': ('City/Town'),
            'is_public': "Show my profile to the public",
            'subscribed_to_email_updates': ('Send me email updates about the EA Hub'),
        }


class EditProfileCauseAreasForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'cause_areas_other',
            'available_to_volunteer',
        )
        labels = {
            'cause_areas_other': ('Other cause areas:'),
            'available_to_volunteer': ('Available to volunteer:')
        }


class EditProfileCareerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'expertise_areas_other',
            'open_to_job_offers',
        )
        labels = {
            'expertise_areas_other': ('Other expertise areas:'),
            'open_to_job_offers': ('Open to job offers:')
        }

class EditProfileCommunityForm(forms.ModelForm):
    local_groups = CustomisedModelMultipleChoiceField(queryset=LocalGroup.objects.all(), required=False, label="Local groups:")

    class Meta:
        model = Profile
        fields = (
            'available_as_speaker',
            'topics_i_speak_about',
            'local_groups',
        )
        labels = {
            'available_as_speaker': ('Available as speaker:'),
            'topics_i_speak_about': ('Topics I speak about:'),
        }

class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

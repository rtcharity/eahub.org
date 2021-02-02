from captcha import fields
from django import forms
from django.conf import settings

from eahub.config.settings import DjangoEnv

from ..localgroups.models import LocalGroup
from .models import Profile, validate_sluggable_name


class CustomisedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class SignupForm(forms.Form):

    name = forms.CharField(
        max_length=200,
        label="First and last name",
        widget=forms.TextInput(attrs={"placeholder": "Name"}),
        validators=[validate_sluggable_name],
    )
    email = forms.EmailField()
    password1 = forms.CharField()
    captcha = fields.ReCaptchaField(
        label="",
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
    )

    field_order = ["name", "email", "password1", "password2", "is_public", "captcha"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.DJANGO_ENV == DjangoEnv.E2E:
            del self.fields["captcha"]

    def signup(self, request, user):
        name = self.cleaned_data["name"]
        Profile.objects.create(user=user, name=name, email_visible=False)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "name",
            "image",
            "linkedin_url",
            "facebook_url",
            "personal_website_url",
            "summary",
            "city_or_town",
            "country",
            "is_public",
            "email_visible",
        )
        widgets = {
            "city_or_town": forms.TextInput(attrs={"placeholder": "London"}),
            "country": forms.TextInput(attrs={"placeholder": "UK"}),
            "linkedin_url": forms.TextInput(),
            "facebook_url": forms.TextInput(),
            "personal_website_url": forms.TextInput(),
            "summary": forms.Textarea(
                attrs={
                    "rows": 7,
                    "placeholder": "In West Philadelphia born and raised. "
                    "On the playground is where I spent most of my days.",
                    "maxlength": 2000,
                }
            ),
        }
        labels = {
            "city_or_town": ("City/Town"),
            "is_public": "Show my profile to the public",
            "email_visible": "Show my email address to other users",
            "linkedin_url": "LinkedIn Profile",
            "facebook_url": "Facebook Profile",
            "personal_website_url": "Personal Website",
        }


class EditProfileCauseAreasForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("cause_areas_other", "available_to_volunteer")
        widgets = {
            "cause_areas_other": forms.Textarea(attrs={"rows": 3, "maxlength": 2000})
        }
        labels = {
            "cause_areas_other": ("Other cause areas:"),
            "available_to_volunteer": ("Available to volunteer:"),
        }


class EditProfileCareerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "expertise_areas_other",
            "open_to_job_offers",
            "career_interest_areas",
        )
        widgets = {
            "expertise_areas_other": forms.Textarea(
                attrs={"rows": 3, "maxlength": 2000}
            )
        }
        labels = {
            "expertise_areas_other": ("Other expertise areas:"),
            "open_to_job_offers": ("Open to job offers:"),
            "career_interest_areas": ("Career interest areas:"),
        }


class EditProfileCommunityForm(forms.ModelForm):
    local_groups = CustomisedModelMultipleChoiceField(
        queryset=LocalGroup.objects.filter(is_public=True),
        required=False,
        label="Local groups:",
    )

    class Meta:
        model = Profile
        fields = (
            "available_as_speaker",
            "topics_i_speak_about",
            "local_groups",
            "offering",
            "looking_for",
        )
        widgets = {
            "topics_i_speak_about": forms.Textarea(
                attrs={"rows": 3, "maxlength": 2000}
            ),
            "offering": forms.Textarea(
                attrs={"rows": 3, "maxlength": 2000, "placeholder": "Teaching python"}
            ),
            "looking_for": forms.Textarea(
                attrs={
                    "rows": 3,
                    "maxlength": 2000,
                    "placeholder": "Chat about wild animal suffering",
                }
            ),
        }
        labels = {
            "available_as_speaker": ("Available as speaker:"),
            "topics_i_speak_about": ("Topics I speak about:"),
            "offering": ("Offering:"),
            "looking_for": ("Looking for:"),
        }


class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)

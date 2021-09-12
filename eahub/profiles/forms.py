import django_select2.forms
from captcha import fields
from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from eahub.config.settings import DjangoEnv

from .models import Profile
from .validators import validate_sluggable_name


class CustomisedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=200,
        validators=[validate_sluggable_name],
    )
    last_name = forms.CharField(
        max_length=200,
        validators=[validate_sluggable_name],
    )
    email = forms.EmailField()
    password1 = forms.CharField()
    captcha = fields.ReCaptchaField(
        label="",
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
    )
    privacy_policy_agreed = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.DJANGO_ENV == DjangoEnv.E2E:
            del self.fields["captcha"]

        community_guidelines_url = reverse_lazy("community_guidelines")
        privacy_policy_url = reverse_lazy("privacy_policy")

        self.fields["privacy_policy_agreed"].label = mark_safe(
            f'I hereby confirm that I have read, understood and agree to the EA Hub <a href="{community_guidelines_url}" target="_blank">Community Guidelines</a> and <a href="{privacy_policy_url}" target="_blank">Privacy Policy.</a>'
        )

    def signup(self, request, user):
        Profile.objects.create(
            user=user,
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
        )


class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "image",
            "linkedin_url",
            "facebook_url",
            "personal_website_url",
            "country",
            "city_or_town",
            "available_to_volunteer",
            "job_title",
            "open_to_job_offers",
            "available_as_speaker",
            "visibility",
            "summary",
            "offering",
            "looking_for",
            "cause_areas_other",
            "expertise_areas_other",
            "topics_i_speak_about",
            "local_groups",
            "allow_messaging",
        ]
        widgets = {
            "local_groups": django_select2.forms.Select2MultipleWidget(
                attrs={
                    "search_fields": [
                        "name__icontains",
                    ]
                }
            )
        }

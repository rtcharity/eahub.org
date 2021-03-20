import django_select2.forms
from captcha import fields
from django import forms
from django.conf import settings
from django.forms import ModelForm

from eahub.config.settings import DjangoEnv

from .models import Profile
from .validators import validate_sluggable_name


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


class DeleteProfileForm(forms.Form):
    confirm = forms.CharField(max_length=100)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "image",
            "linkedin_url",
            "facebook_url",
            "personal_website_url",
            "country",
            "city_or_town",
            "available_to_volunteer",
            "open_to_job_offers",
            "available_as_speaker",
            "email_visible",
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

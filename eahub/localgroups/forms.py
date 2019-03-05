from django import forms

from . import models
from ..base import models as base_models
from ..profiles import models as profiles_models


def unwrap_user(value):
    if isinstance(value, base_models.User):
        return value.profile
    return value


class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, **kwargs):
        forms.ModelMultipleChoiceField.__init__(
            self,
            queryset=profiles_models.Profile.objects.all(),
            to_field_name="slug",
            **kwargs,
        )

    def label_from_instance(self, obj):
        return obj.name

    def clean(self, value):
        return base_models.User.objects.filter(profile__in=super().clean(value))

    def prepare_value(self, value):
        if hasattr(value, "__iter__"):
            return super().prepare_value(map(unwrap_user, value))
        return super().prepare_value(unwrap_user(value))


class LocalGroupForm(forms.ModelForm):
    organisers = UserMultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control multiselect-form"}),
    )

    class Meta:
        model = models.LocalGroup
        fields = [
            "name",
            "local_group_type",
            "city_or_town",
            "country",
            "website",
            "facebook_group",
            "facebook_page",
            "email",
            "meetup_url",
            "organisers",
        ]

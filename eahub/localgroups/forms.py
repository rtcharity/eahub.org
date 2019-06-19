from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from ..base import models as base_models
from ..profiles import models as profiles_models
from . import models as localgroups_models


class OrganiserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *, user, local_group, past_organisers, **kwargs):
        if local_group is None or local_group.pk is None:
            already_selected = models.Value(False, output_field=models.BooleanField())
        elif past_organisers:
            already_selected = models.Case(
                models.When(pk__in=local_group.past_organisers.all(), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        else:
            already_selected = models.Case(
                models.When(pk__in=local_group.organisers.all(), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        queryset = base_models.User.objects.select_related("profile").annotate(
            already_selected=already_selected
        )
        queryset = queryset.order_by(
            "-already_selected", "profile__name", "profile__slug", "email"
        )
        forms.ModelMultipleChoiceField.__init__(self, queryset=queryset, **kwargs)

    def label_from_instance(self, value):
        try:
            profile = value.profile
        except profiles_models.Profile.DoesNotExist:
            return value.email
        return profile.name

    def prepare_value(self, value):
        if isinstance(value, base_models.User):
            try:
                profile = value.profile
            except profiles_models.Profile.DoesNotExist:
                return value.email
            return profile.slug
        if hasattr(value, "__iter__") and not isinstance(value, str):
            return list(map(self.prepare_value, value))
        return super().prepare_value(value)

    def _check_values(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages["list"], code="list")
        slugs = set()
        emails = set()
        for subvalue in value:
            if not isinstance(subvalue, str):
                raise ValidationError(self.error_messages["list"], code="list")
            if "@" in subvalue:
                emails.add(subvalue)
            else:
                slugs.add(subvalue)
        qs = self.queryset.filter(
            models.Q(profile__slug__in=slugs)
            | models.Q(profile__isnull=True, email__in=emails)
        )
        keys = {self.prepare_value(user) for user in qs}
        for subvalue in value:
            if subvalue not in keys:
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": subvalue},
                )
        return qs


class LocalGroupForm(forms.ModelForm):
    def __init__(self, *, user, instance=None, **kwargs):
        forms.ModelForm.__init__(self, instance=instance, **kwargs)
        self.fields["organisers"] = OrganiserMultipleChoiceField(
            user=user,
            local_group=instance,
            past_organisers=False,
            required=False,
            widget=forms.SelectMultiple(
                attrs={"class": "form-control multiselect-form"}
            ),
        )
        self.fields["past_organisers"] = OrganiserMultipleChoiceField(
            user=user,
            local_group=instance,
            past_organisers=True,
            required=False,
            widget=forms.SelectMultiple(
                attrs={"class": "form-control multiselect-form"}
            ),
        )

    class Meta:
        model = localgroups_models.LocalGroup
        fields = [
            "name",
            "is_active",
            "local_group_type",
            "city_or_town",
            "country",
            "website",
            "facebook_group",
            "facebook_page",
            "email",
            "meetup_url",
            "organisers",
            "past_organisers",
        ]

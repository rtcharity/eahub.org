import django_select2.forms
import us
from django import forms
from django.core.exceptions import ValidationError
from django.db import models

from eahub.base import models as base_models
from eahub.localgroups.models import LocalGroup, LocalGroupType
from eahub.profiles import models as profiles_models
from eahub.profiles.models import VisibilityEnum


class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *, user, local_group, **kwargs):
        if local_group is None or local_group.pk is None:
            already_selected = models.Value(False, output_field=models.BooleanField())
        else:
            already_selected = models.Case(
                models.When(pk__in=local_group.organisers.all(), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        queryset = base_models.User.objects.select_related("profile").annotate(
            already_selected=already_selected
        )
        queryset = queryset.filter(
            models.Q(
                profile__visibility=VisibilityEnum.PUBLIC, profile__is_approved=True
            )
            | models.Q(already_selected=True)
            | models.Q(pk=user.pk)
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
        return profile.get_full_name()

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
        self.fields["organisers"] = UserMultipleChoiceField(
            user=user,
            local_group=instance,
            required=False,
            widget=django_select2.forms.Select2MultipleWidget(),
        )
        self.fields["local_group_types"] = forms.MultipleChoiceField(
            widget=django_select2.forms.Select2MultipleWidget(),
            required=False,
            choices=LocalGroupType.choices(),
        )

    def clean(self):
        data = self.cleaned_data
        if (
            data["country"]
            in ["United States", "US", "USA", "United States of America"]
            and data["region"]
        ):
            state = us.states.lookup(data["region"])
            if state is None:
                raise forms.ValidationError(
                    f"'{data['region']}' is not a valid US state"
                )
            data["region"] = state.name
        return data

    class Meta:
        model = LocalGroup
        fields = [
            "name",
            "is_active",
            "local_group_types",
            "city_or_town",
            "region",
            "country",
            "website",
            "other_website",
            "facebook_group",
            "facebook_page",
            "email",
            "meetup_url",
            "organisers",
            "organisers_freetext",
            "other_info",
        ]
        labels = {
            "organisers_freetext": "Organisers (not on EAHub)",
            "region": "Region (e.g., US state, if applicable)",
            "website": (
                "<br><div style='font-size: 16px; font-weight: normal;'>"
                "Please enter all the ways potential group members can currently "
                "connect with your group:</div><br><br> Website"
            ),
        }
        help_texts = {
            "name": "University groups: Ideally avoid acronyms in your group name "
            "unless they are likely to be unique worldwide. If the name of "
            "your university is also the name of a city, indicate in the name "
            "that this is a university group."
        }

    def clean_local_group_types(self):
        return list(map(int, self.cleaned_data["local_group_types"]))

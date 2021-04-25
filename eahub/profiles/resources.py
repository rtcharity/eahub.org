import re
from typing import Any, List, Optional

from import_export import fields
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import ManyToManyWidget, Widget

from eahub.base.models import User
from eahub.profiles.models import (
    Profile,
    ProfileAnalyticsLog,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)


class ProfileTagWidget(ManyToManyWidget):
    def __init__(
        self,
        enum_types: List[ProfileTagTypeEnum],
        *args,
        **kwargs,
    ):
        self.enum_types = enum_types
        super().__init__(model=ProfileTag, field="name", *args, **kwargs)

    def clean(self, value: str, row: dict = None, *args, **kwargs) -> List[ProfileTag]:
        if not value:
            return self.model.objects.none()

        is_eag_import = "\n" in value
        separator = "\n" if is_eag_import else ";"
        tag_names: List[str] = value.split(separator)
        tags = []
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            tag_existing = ProfileTag.objects.filter(name__iexact=tag_name).first()
            if tag_existing:
                tag = tag_existing
            else:
                tag = ProfileTag.objects.create(name=tag_name)

            tag_types = []
            for enum_type in self.enum_types:
                tag_types.append(ProfileTagType.objects.get(type=enum_type))
            tag.types.add(*tag_types)
            tag.save()

            tags.append(tag)
        return tags


class UserWidget(Widget):
    def clean(self, value: Any, row=None, *args, **kwargs) -> Optional[User]:
        return User.objects.get_or_create(email=value)[0]


class ProfileResource(ModelResource):
    user = fields.Field(
        attribute="user",
        widget=UserWidget(),
    )
    tags_career_stage = fields.Field(
        attribute="tags_career_stage",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.CAREER_STAGE],
        ),
    )
    tags_university = fields.Field(
        attribute="tags_university",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.UNIVERSITY],
        ),
    )
    tags_ea_involvement = fields.Field(
        attribute="tags_ea_involvement",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.EA_INVOLVEMENT],
        ),
    )
    tags_expertise_area = fields.Field(
        attribute="tags_expertise_area",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.EXPERTISE_AREA],
        ),
    )
    tags_cause_area_expertise = fields.Field(
        attribute="tags_cause_area_expertise",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.CAUSE_AREA_EXPERTISE],
        ),
    )
    tags_cause_area = fields.Field(
        attribute="tags_cause_area",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.CAUSE_AREA],
        ),
    )
    tags_career_interest = fields.Field(
        attribute="tags_career_interest",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.CAREER_INTEREST],
        ),
    )
    tags_affiliation = fields.Field(
        attribute="tags_affiliation",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.AFFILIATION],
        ),
    )
    tags_organisational_affiliation = fields.Field(
        attribute="tags_organisational_affiliation",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.ORGANISATIONAL_AFFILIATION],
        ),
    )
    tags_speech_topic = fields.Field(
        attribute="tags_speech_topic",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.SPEECH_TOPIC],
        ),
    )

    class Meta:
        model = Profile
        import_id_fields = [
            "user",
        ]
        fields = [
            "user",
            "first_name",
            "last_name",
            "organization",
            "study_subject",
            "job_title",
            "is_hiring",
            "available_to_volunteer",
            "linkedin_url",
            "facebook_url",
            "facebook_url",
            "calendly_url",
            "twitter",
            "personal_website_url",
            "country",
            "city_or_town",
            "linkedin",
            "tags_career_stage",
            "tags_university",
            "tags_ea_involvement",
            "tags_expertise_area",
            "tags_cause_area_expertise",
            "tags_cause_area",
            "tags_career_interest",
            "tags_affiliation",
        ]

    def import_field(
        self, field: Field, obj: Profile, data: dict, is_m2m: bool = False
    ):
        if field.column_name == "linkedin_url":
            match = re.search(
                r"(?P<bio_before>.*)(?P<url>(https://www\.)?((linkedin.com|linked.in)(/in)?/[a-z0-9](-?[a-z0-9])*)/?)?(?P<bio_after>.*)",
                data[field.attribute],
            )
            if match.group("url"):
                obj.linkedin_url = match.group("url")
            if match.group("bio_before") or match.group("bio_after"):
                obj.summary += f"{match.group('bio_before')} {match.group('bio_after')}"
        else:
            super().import_field(field, obj, data, is_m2m)

    def skip_row(self, instance, original) -> bool:
        is_profile_exists = getattr(original, "pk") is not None
        return is_profile_exists


class ProfileAnalyticsResource(ModelResource):
    class Meta:
        model = ProfileAnalyticsLog
        export_order = [
            "id",
            "profile",
            "time",
            "action",
            "action_uuid",
            "field",
            "new_value",
            "old_value",
        ]

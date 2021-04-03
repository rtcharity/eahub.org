from typing import Any, List, Optional

from import_export import fields
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
        tag_names: List[str] = value.split(";")
        tags = []
        for tag_name in tag_names:
            tag, is_created = ProfileTag.objects.get_or_create(
                name=tag_name,
            )
            if is_created:
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
            enum_types=[
                ProfileTagTypeEnum.EXPERTISE_AREA,
                ProfileTagTypeEnum.CAUSE_AREA,
            ],
        ),
    )
    tags_career_interest = fields.Field(
        attribute="tags_career_interest",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.CAREER_INTEREST],
        ),
    )
    tags_generic = fields.Field(
        attribute="tags_generic",
        widget=ProfileTagWidget(
            enum_types=[ProfileTagTypeEnum.GENERIC],
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
            "personal_website_url",
            "country",
            "city_or_town",
            "linkedin",
            "tags_career_stage",
            "tags_university",
            "tags_ea_involvement",
            "tags_expertise_area",
            "tags_career_interest",
            "tags_generic",
        ]


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

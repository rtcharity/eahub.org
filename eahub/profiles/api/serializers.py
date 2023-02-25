from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from eahub.profiles.models import (
    Profile,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)


# https://www.django-rest-framework.org/api-guide/fields/#listfield
class StringListField(serializers.ListField):   
    child = serializers.CharField()


class TagTypeSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProfileTagType
        fields = [
            "type",
        ]


class TagSerializer(serializers.ModelSerializer):
    types = TagTypeSerializer(many=True)

    class Meta:
        model = ProfileTag
        fields = [
            "pk",
            "name",
            "types",
            "count",
        ]


class ProfileSerializer(serializers.ModelSerializer):

    for tag_type_enum in ProfileTagTypeEnum:
        locals()[f"tags_{tag_type_enum.value}"] = TagSerializer(
            many=True, required=False
        )
        locals()[f"tags_{tag_type_enum.value}_pks"] = PrimaryKeyRelatedField(
            many=True,
            queryset=ProfileTag.objects.filter(types__type=tag_type_enum),
            source=f"tags_{tag_type_enum.value}",
            required=False,
        )

    class Meta:
        model = Profile
        fields = []
        for tag_type_enum in ProfileTagTypeEnum:
            fields.append(f"tags_{tag_type_enum.value}")
            fields.append(f"tags_{tag_type_enum.value}_pks")

    def update(self, instance: Profile, validated_data: dict) -> Profile:
        for field in self.Meta.fields:
            is_updatable_field = not field.endswith("_pks")
            if is_updatable_field:
                self._m2m_field_update(
                    instance,
                    validated_data=validated_data,
                    field_name=field,
                )
        return super().update(instance, validated_data)

    def _m2m_field_update(
        self,
        instance: Profile,
        validated_data: dict,
        field_name: str,
    ):
        if field_name in validated_data:
            tags_new = validated_data.pop(field_name)
            tags_field = getattr(instance, field_name)
            tags_field.set(tags_new)


class SimilaritySearchProfileSerializer(serializers.ModelSerializer):

    # see also class ProfilePublicIndex at eahub\profiles\index.py
    # see also class Profile at eahub\profiles\models.py

    url = serializers.CharField(source='get_absolute_url')
    image = serializers.CharField(source='get_image_url')
    name = serializers.CharField(source='get_full_name')
    messaging_url = serializers.CharField(source='get_messaging_url_if_can_receive_message')

    local_groups = StringListField(source='get_local_groups_formatted')
    expertise = StringListField(source='get_tags_expertise_formatted')
    cause_areas = StringListField(source='get_tags_cause_area_formatted')

    class Meta:
        model = Profile
        fields = [
            "url",
            "image",
            # "objectID",
            "name",
            "job_title",
            "available_to_volunteer",
            "open_to_job_offers",
            "available_as_speaker",
            "is_organiser",
            "country",
            "city_or_town",   # verbose_name="City"
            "messaging_url",
            "personal_website_url",
            "linkedin_url",
            "facebook_url",
            "local_groups",
            "summary",
            "offering",
            "looking_for",
            "expertise",
            "expertise_areas_other",
            "cause_areas",
            "cause_areas_other",
        ]

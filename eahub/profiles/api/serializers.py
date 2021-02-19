from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from eahub.profiles.models import (
    Profile,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)


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
    tags_generic = TagSerializer(many=True, required=False)
    tags_generic_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.GENERIC),
        source=f"tags_{ProfileTagTypeEnum.GENERIC.value}",
        required=False,
    )
    tags_expertise_area = TagSerializer(many=True, required=False)
    tags_expertise_area_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.filter(
            types__type=ProfileTagTypeEnum.EXPERTISE_AREA
        ),
        source=f"tags_{ProfileTagTypeEnum.EXPERTISE_AREA.value}",
        required=False,
    )
    tags_cause_area = TagSerializer(many=True, required=False)
    tags_cause_area_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,  # todo redundant?
        queryset=ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.CAUSE_AREA),
        source=f"tags_{ProfileTagTypeEnum.CAUSE_AREA.value}",
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "tags_generic",
            "tags_generic_pks",
            "tags_expertise_area",
            "tags_expertise_area_pks",
            "tags_cause_area",
            "tags_cause_area_pks",
        ]

    def update(self, instance: Profile, validated_data: dict) -> Profile:
        self._m2m_field_update(instance, validated_data, field_name="tags_generic")
        self._m2m_field_update(
            instance, validated_data, field_name="tags_expertise_area"
        )
        self._m2m_field_update(instance, validated_data, field_name="tags_cause_area")
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

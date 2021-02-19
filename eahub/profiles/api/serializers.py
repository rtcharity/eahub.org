from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from eahub.profiles.models import Profile, ProfileTag, ProfileTagTypeEnum
from eahub.profiles.models import ProfileTagType


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
        ]


class ProfileSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    tags_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.all(),
        source="tags",
        required=False,
    )
    expertise_areas_new = TagSerializer(many=True, required=False)
    expertise_areas_new_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.EXPERTISE),
        source="expertise_areas_new",
        required=False,
    )
    cause_areas_new = TagSerializer(many=True, required=False)
    cause_areas_new_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.CAUSE_AREA),
        source="cause_areas_new",
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "tags",
            "tags_pks",
            "expertise_areas_new",
            "expertise_areas_new_pks",
            "cause_areas_new",
            "cause_areas_new_pks",
        ]

    def update(self, instance: Profile, validated_data: dict, **kwargs) -> Profile:
        self._m2m_field_update(instance, validated_data, field_name="tags")
        self._m2m_field_update(
            instance, validated_data, field_name="expertise_areas_new"
        )
        self._m2m_field_update(instance, validated_data, field_name="cause_areas_new")
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

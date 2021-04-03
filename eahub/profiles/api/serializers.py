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

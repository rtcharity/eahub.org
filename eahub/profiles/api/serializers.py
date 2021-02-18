from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from eahub.profiles.models import Profile, ProfileTag, ProfileTagTypeEnum


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTag
        fields = [
            "pk",
            "name",
            "types",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    causes = TagSerializer(many=True, required=False)
    causes_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.filter(types__type=ProfileTagTypeEnum.CAUSE_AREA),
        source="causes",
        required=False,
    )
    tags = TagSerializer(many=True, required=False)
    tags_pks = PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=ProfileTag.objects.all(),
        source="tags",
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "tags",
            "tags_pks",
            "causes",
            "causes_pks",
        ]

    def update(self, instance: Profile, validated_data: dict, **kwargs) -> Profile:
        if "tags" in validated_data:
            tags_new = validated_data.pop("tags")
            instance.tags.set(tags_new)
            instance.save()
        if "causes" in validated_data:
            causes_new = validated_data.pop("causes")
            instance.causes.set(causes_new)
            instance.save()
        return super().update(instance, validated_data)

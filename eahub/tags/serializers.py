from typing import Type

from django.db import models
from enumfields import Enum
from enumfields.drf import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer


def tag_model_serializer_factory(
    tag_type_model_cls: Type[models.Model],
    tag_model_cls: Type[models.Model],
) -> type:
    class TagTypeSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
        class Meta:
            model = tag_type_model_cls
            fields = [
                "type",
            ]

    class TagSerializer(serializers.ModelSerializer):
        types = TagTypeSerializer(many=True)

        class Meta:
            model = tag_model_cls
            fields = [
                "pk",
                "name",
                "types",
                "count",
            ]

    return TagSerializer


def tagged_model_serializer_factory(
    tagged_model_cls: Type[models.Model],
    tag_model_cls: Type[models.Model],
    tag_type_model_cls: Type[models.Model],
    tag_type_enum: Type[Enum],
) -> type:

    TagSerializer = tag_model_serializer_factory(
        tag_type_model_cls=tag_type_model_cls,
        tag_model_cls=tag_model_cls,
    )

    class TaggedModelSerializer(ModelSerializer):

        for tag_type_enum_member in tag_type_enum:
            locals()[f"tags_{tag_type_enum_member.value}"] = TagSerializer(
                many=True, required=False
            )
            locals()[f"tags_{tag_type_enum_member.value}_pks"] = PrimaryKeyRelatedField(
                many=True,
                queryset=tag_model_cls.objects.filter(types__type=tag_type_enum_member),
                source=f"tags_{tag_type_enum_member.value}",
                required=False,
            )

        def update(self, instance, validated_data: dict) -> Type[models.Model]:
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
            instance: Type[models.Model],
            validated_data: dict,
            field_name: str,
        ):
            if field_name in validated_data:
                tags_new = validated_data.pop(field_name)
                tags_field = getattr(instance, field_name)
                tags_field.set(tags_new)

        class Meta:
            model = tagged_model_cls
            fields = []
            for tag_type_enum_member in tag_type_enum:
                fields.append(f"tags_{tag_type_enum_member.value}")
                fields.append(f"tags_{tag_type_enum_member.value}_pks")

    return TaggedModelSerializer

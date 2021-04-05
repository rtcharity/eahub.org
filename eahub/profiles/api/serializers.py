from eahub.profiles.models import (
    Profile,
    ProfileTag,
    ProfileTagType,
    ProfileTagTypeEnum,
)
from eahub.tags.serializers import tag_model_serializer_factory
from eahub.tags.serializers import tagged_model_serializer_factory


ProfileSerializer = tagged_model_serializer_factory(
    tagged_model_cls=Profile,
    tag_model_cls=ProfileTag,
    tag_type_model_cls=ProfileTagType,
    tag_type_enum=ProfileTagTypeEnum,
)
ProfileTagSerializer = tag_model_serializer_factory(
    tag_type_model_cls=ProfileTagType, tag_model_cls=ProfileTag
)

from eahub.jobs.models import Job, JobTag, JobTagType, JobTagTypeEnum
from eahub.tags.serializers import (
    tag_model_serializer_factory,
    tagged_model_serializer_factory,
)

JobSerializer = tagged_model_serializer_factory(
    tagged_model_cls=Job,
    tag_model_cls=JobTag,
    tag_type_model_cls=JobTagType,
    tag_type_enum=JobTagTypeEnum,
)
JobTagSerializer = tag_model_serializer_factory(
    tag_type_model_cls=JobTagType, tag_model_cls=JobTag
)

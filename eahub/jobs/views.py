from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from eahub.jobs.models import Job
from eahub.jobs.models import JobTag
from eahub.jobs.models import JobTagStatus
from eahub.jobs.models import JobTagType
from eahub.jobs.serializers import JobSerializer
from eahub.jobs.serializers import JobTagSerializer
from eahub.tags.views import create_tag_view_factory


class JobViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Job.objects.filter()
    serializer_class = JobSerializer


create_tag_view = create_tag_view_factory(
    tag_model=JobTag,
    tagged_model=Job,
    tag_status_enum=JobTagStatus,
    tag_type_model=JobTagType,
    tag_serializer=JobTagSerializer,
)

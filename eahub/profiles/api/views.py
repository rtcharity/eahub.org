from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from eahub.profiles.api.serializers import ProfileSerializer, ProfileTagSerializer
from eahub.profiles.models import Profile, ProfileTag, ProfileTagStatus, ProfileTagType
from eahub.tags.views import create_tag_view_factory


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer


create_tag_view = create_tag_view_factory(
    tag_model=ProfileTag,
    tagged_model=Profile,
    tag_status_enum=ProfileTagStatus,
    tag_type_model=ProfileTagType,
    tag_serializer=ProfileTagSerializer,
)

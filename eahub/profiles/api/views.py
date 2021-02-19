from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eahub.profiles.api.serializers import ProfileSerializer
from eahub.profiles.api.serializers import TagSerializer
from eahub.profiles.models import Profile
from eahub.profiles.models import ProfileTag
from eahub.profiles.models import ProfileTagType


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_tag_view(request: Response):
    tag = ProfileTag.objects.create(
        name=request.data["name"], author=Profile.objects.get(user=request.user)
    )
    tag_type = ProfileTagType.objects.get_or_create(type=request.data["type"])[0]
    tag.types.add(tag_type)
    return Response(TagSerializer(tag).data)

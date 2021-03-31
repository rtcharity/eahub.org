from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eahub.profiles.api.serializers import ProfileSerializer, TagSerializer
from eahub.profiles.models import Profile, ProfileTag, ProfileTagStatus, ProfileTagType


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_tag_view(request: Request) -> Response:
    tag, is_created = ProfileTag.objects.get_or_create(
        name=request.data["name"].strip(),
    )
    if is_created:
        tag.author = Profile.objects.get(user=request.user)
        tag.status = ProfileTagStatus.PENDING

    tag_type = ProfileTagType.objects.get(type=request.data["type"])
    tag.types.add(tag_type)
    tag.save()
    return Response(TagSerializer(tag).data)

from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eahub.profiles.api.serializers import ProfileSerializer, TagSerializer
from eahub.profiles.api.serializers import SimilaritySearchProfileSerializer
from eahub.profiles.models import Profile, ProfileTag, ProfileTagStatus, ProfileTagType
from eahub.profiles.models import VisibilityEnum


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
    tag_name = request.data["name"].strip()
    tag = ProfileTag.objects.filter(name__iexact=tag_name).first()
    if not tag:
        tag = ProfileTag.objects.create(
            name=tag_name,
            author=Profile.objects.get(user=request.user),
            status=ProfileTagStatus.PENDING,
        )

    tag_type = ProfileTagType.objects.get(type=request.data["type"])
    tag.types.add(tag_type)
    tag.save()
    return Response(TagSerializer(tag).data)


@api_view(["GET"])
def similarity_search_view(request: Request) -> Response:
    profile_id = request.query_params["id"].strip()   # https://www.django-rest-framework.org/api-guide/requests/

    profile = Profile.objects.filter(   # see def is_searchable_public()
                  is_approved=True, 
                  visibility=VisibilityEnum.PUBLIC,   # TODO: when should we use [VisibilityEnum.INTERNAL, VisibilityEnum.PUBLIC] ?
                  user__is_active=True, 
                  id=profile_id   # for debugging, TODO: remove later
              ).first()

    # TODO: similarity search

    return Response(SimilaritySearchProfileSerializer(
        [profile, profile, profile],   # TODO: return similarity search results not profile
        many=True
    ).data)

from collections import Callable
from typing import Type

from django.db.models import Model
from enumfields import Enum
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from eahub.tags.models import Tag


def create_tag_view_factory(
    tag_model: Type[Tag],
    tagged_model: Type[Model],
    tag_status_enum: Type[Enum],
    tag_type_model: Type[Model],
    tag_serializer: Type[ModelSerializer],
) -> Callable:
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def create_tag_view(request: Request) -> Response:
        tag, is_created = tag_model.objects.get_or_create(
            name=request.data["name"].strip(),
        )
        if is_created:
            tag.author = tagged_model.objects.get(user=request.user)
            tag.status = tag_status_enum.PENDING

        tag_type = tag_type_model.objects.get(type=request.data["type"])
        tag.types.add(tag_type)
        tag.save()

        return Response(tag_serializer(tag).data)

    return create_tag_view

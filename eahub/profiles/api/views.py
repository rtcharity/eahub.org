from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from eahub.profiles.api.serializers import ProfileSerializer
from eahub.profiles.models import Profile


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    queryset = Profile.objects.filter(user__is_active=True)
    serializer_class = ProfileSerializer

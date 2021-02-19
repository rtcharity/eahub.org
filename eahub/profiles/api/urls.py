from django.urls import path
from rest_framework.routers import DefaultRouter

from eahub.profiles.api.views import ProfileViewSet, create_tag_view

app_name = "profiles_api"

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)


urlpatterns = [
    path("profiles/tags/create/", create_tag_view),
] + router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter

from eahub.profiles.api.views import ProfileViewSet, create_tag_view
from eahub.profiles.api.views import similarity_search_view

app_name = "profiles_api"

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)


urlpatterns = [
    path("profiles/tags/create/", create_tag_view),
    path("profiles/similaritySearch/", similarity_search_view),
] + router.urls

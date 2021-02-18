from rest_framework.routers import DefaultRouter

from eahub.profiles.api.views import ProfileViewSet

app_name = "profiles_api"

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)


urlpatterns = router.urls

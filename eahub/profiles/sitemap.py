from django.contrib.sitemaps import GenericSitemap
from django.db.models import QuerySet

from eahub.profiles.models import Profile, VisibilityEnum


class ProfilesSitemap(GenericSitemap):
    def items(self) -> QuerySet:
        return Profile.objects.filter(
            is_approved=True, visibility=VisibilityEnum.PUBLIC, user__is_active=True
        )

import fnmatch
import logging

from allauth.account import adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.conf import settings
from django.core import exceptions
from django.http import HttpRequest

from eahub.base.models import User
from eahub.profiles.models import Profile


logger = logging.getLogger(__name__)


class EmailBlacklistingAdapter(adapter.DefaultAccountAdapter):
    def clean_email(self, email):
        if any(
            fnmatch.fnmatch(email, pattern)
            for pattern in settings.BLACKLISTED_EMAIL_PATTERNS
        ):
            raise exceptions.ValidationError(
                "Due to ongoing abuse issues, we're not currently accepting signups "
                "from this email address. Please get in touch via the contact form if "
                "you have questions.",
                code="blacklisted",
            )
        return email


class EAHubSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request: HttpRequest, sociallogin: SocialLogin, form=None) -> User:
        user: User = super().save_user(request, sociallogin, form)
        Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return user

    def pre_social_login(self, request: HttpRequest, sociallogin: SocialLogin):
        try:
            user = User.objects.get(email=sociallogin.user.email)
            try:
                sociallogin.connect(request, user)
            except:
                logger.exception("user SSO connection failed")
        except User.DoesNotExist:
            pass

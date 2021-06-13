import fnmatch

from allauth.account import adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin
from django.conf import settings
from django.core import exceptions
from django.http import HttpRequest
from django.urls import reverse

from eahub.base.models import User
from eahub.profiles.models import Profile


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

    def get_login_redirect_url(self, request: HttpRequest) -> str:
        redirect_url = request.POST.get("next", "")
        if redirect_url:
            return redirect_url
        else:
            return reverse(settings.LOGIN_REDIRECT_URL)


class EAHubSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(
        self, request: HttpRequest, sociallogin: SocialLogin, form=None
    ) -> User:
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
                # ie the user already has connected SSO
                pass
        except User.DoesNotExist:
            pass

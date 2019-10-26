import fnmatch

from allauth.account import adapter
from django.conf import settings
from django.core import exceptions


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

from allauth.account.models import EmailAddress
from django.urls import reverse

from eahub.base.models import User
from eahub.tests.e2e.cases import E2ETestCase


class SignUpTest(E2ETestCase):
    def test_signup(self):
        user_email = "test@eahub.org"
        user_password = "Wa4@;fh>A/~W#6SH"

        self.selenium.get(self.live_server_url)

        self.find("#signup-btn").click()

        self.find("[name='name']").send_keys("Test User")
        self.find("[name='email']").send_keys(user_email)
        self.find("[name='password1']").send_keys(user_password)

        self.find("form button[type='submit']").click()

        self.find(".verification-sent")

        User.objects.get(email=user_email)
        email_address = EmailAddress.objects.get(email=user_email)
        email_address.verified = True
        email_address.save()

        self.selenium.get(self.live_server_url + reverse("account_login"))
        self.find("#id_login").send_keys(user_email)
        self.find("#id_password").send_keys(user_password)
        self.find("#submit").click()
        self.selenium.get(self.live_server_url + reverse("my_profile"))
        self.find(".profile-info.profile-cards")

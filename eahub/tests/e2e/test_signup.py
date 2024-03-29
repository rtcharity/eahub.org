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

        self.find("[name='first_name']").send_keys("Test")
        self.find("[name='last_name']").send_keys("User")
        self.find("[name='email']").send_keys(user_email)
        self.find("[name='password1']").send_keys(user_password)
        self.find("[name='privacy_policy_agreed'").click()

        self.find("form button[type='submit']").click()

        self.find(".verification-sent")

        User.objects.get(email=user_email)
        email_address = EmailAddress.objects.get(email=user_email)
        email_address.verified = True
        email_address.save()

        self.selenium.get(self.live_server_url + reverse("account_login"))
        self.find("[name='login']").send_keys(user_email)
        self.find("[name='password']").send_keys(user_password)
        self.find("[type='submit']").click()
        self.selenium.get(self.live_server_url + reverse("profiles_app:my_profile"))
        self.find(".prof__btns .btn")

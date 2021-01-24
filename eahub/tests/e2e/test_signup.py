from django.urls import reverse

from eahub.base.models import User
from eahub.tests.e2e.cases import E2ETestCase


class SignUpTest(E2ETestCase):
    def test_signup(self):
        email = "test@eahub.org"
        password = "Wa4@;fh>A/~W#6SH"

        self.selenium.get(self.live_server_url)

        self.find("#navbar_signup").click()

        self.find("#id_name").send_keys("Test User")
        self.find("#id_email").send_keys(email)
        self.find("#id_password1").send_keys(password)
        self.find("#id_password2").send_keys(password)
        self.find("#id_is_public").click()

        self.find("#submit").click()

        self.find(".profile-welcome")

        user = User.objects.get(email=email)

        self.assertEquals(user.email, email)

        self.selenium.get(self.live_server_url + reverse("account_logout"))

        self.find("#navbar_login").click()

        self.find("#id_login")
        self.find("#id_login").send_keys(email)
        self.find("#id_password").send_keys(password)
        self.find("#submit").click()
        self.selenium.get(self.live_server_url + reverse("my_profile"))
        self.find(".profile-info.profile-cards")

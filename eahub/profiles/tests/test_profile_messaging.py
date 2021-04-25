from django.core import mail
from django.template.response import TemplateResponse
from django.urls import reverse

from eahub.profiles.models import VisibilityEnum
from eahub.tests.cases import EAHubTestCase


class ProfileMessagingTestCase(EAHubTestCase):
    def test_save_analytics_on_profile_creation(self):
        profile_sender = self.gen.profile()
        profile_recipient = self.gen.profile(visibility=VisibilityEnum.INTERNAL)
        message_body = "test message body"
        self.client.force_login(profile_sender.user)
        response: TemplateResponse = self.client.post(
            path=reverse("profiles_app:message_profile", args=[profile_recipient.slug]),
            data=dict(
                your_name=profile_sender.get_full_name(),
                your_email_address=profile_sender.user.email,
                your_message=message_body,
            ),
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertIn(message_body, mail.outbox[0].body)

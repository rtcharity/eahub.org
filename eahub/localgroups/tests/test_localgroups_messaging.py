from django.core import mail
from django.template.response import TemplateResponse
from django.urls import reverse

from eahub.localgroups.models import Organisership
from eahub.tests.cases import EAHubTestCase


class LocalGroupsMessagingTestCase(EAHubTestCase):
    def test_group_messaging(self):
        profile_sender = self.gen.profile()
        localgroup_recipient = self.gen.group()
        profile_organiser = self.gen.profile()
        o1 = Organisership(
            user=profile_organiser.user, local_group=localgroup_recipient
        )
        o1.save()

        message_body = "test message body"
        self.client.force_login(profile_sender.user)
        response: TemplateResponse = self.client.post(
            path=reverse("message_group", args=[localgroup_recipient.slug]),
            data=dict(
                your_name=profile_sender.get_full_name(),
                your_email_address=profile_sender.user.email,
                your_message=message_body,
            ),
            follow=True,
        )
        self.assertEqual(200, response.status_code)
        self.assertIn(message_body, mail.outbox[0].body)
        self.assertEqual("EA Hub <admin@eahub.org>", mail.outbox[0].from_email)
        self.assertEqual(profile_organiser.user.email, mail.outbox[0].to[0][0])

    def test_group_messaging_not_to_users_with_messaging_disabled(self):
        profile_sender = self.gen.profile()
        localgroup_recipient = self.gen.group()
        profile_organiser = self.gen.profile(allow_messaging=False)
        o1 = Organisership(
            user=profile_organiser.user, local_group=localgroup_recipient
        )
        o1.save()

        message_body = "test message body"
        self.client.force_login(profile_sender.user)
        response: TemplateResponse = self.client.post(
            path=reverse("message_group", args=[localgroup_recipient.slug]),
            data=dict(
                your_name=profile_sender.get_full_name(),
                your_email_address=profile_sender.user.email,
                your_message=message_body,
            ),
            follow=True,
        )
        self.assertEqual(500, response.status_code)

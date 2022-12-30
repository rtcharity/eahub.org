from django.core import mail
from django.template.response import TemplateResponse
from django.urls import reverse
import pytest

from eahub.base.models import MessagingLog
from eahub.localgroups.models import Organisership
from eahub.tests.cases import EAHubTestCase


class LocalGroupsMessagingTestCase(EAHubTestCase):
    @pytest.mark.skip(reason="Not needed because of groups redirect")
    def test_group_messaging_sends_to_group_email(self):
        profile_sender = self.gen.profile()
        localgroup_recipient = self.gen.group(email="group@test.com")

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
        self.assertEqual(localgroup_recipient.email, mail.outbox[0].to[0])

        self.assertEqual(
            "GROUP",
            MessagingLog.objects.filter(
                sender_email=profile_sender.user.email,
                recipient_email=localgroup_recipient.email,
            )[0].recipient_type,
        )

    @pytest.mark.skip(reason="Not needed because of groups redirect")
    def test_group_messaging_sends_to_first_organiser(self):
        profile_sender = self.gen.profile()

        profile_organiser = self.gen.profile()
        profile_organiser_2 = self.gen.profile()
        localgroup_recipient = self.gen.group(
            organisers=[profile_organiser.user, profile_organiser_2.user]
        )

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

        first_organiser = sorted(
            [profile_organiser.user.email, profile_organiser_2.user.email]
        )[0]

        self.assertEqual(200, response.status_code)
        self.assertIn(message_body, mail.outbox[0].body)
        self.assertEqual("EA Hub <admin@eahub.org>", mail.outbox[0].from_email)
        self.assertEqual(first_organiser, mail.outbox[0].to[0])

        self.assertEqual(
            "GROUP",
            MessagingLog.objects.filter(
                sender_email=profile_sender.user.email, recipient_email=first_organiser
            )[0].recipient_type,
        )

    def test_group_messaging_throws_if_no_available_emails(self):
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

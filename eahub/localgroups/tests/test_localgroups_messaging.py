from django.core import mail
from django.template.response import TemplateResponse
from django.urls import reverse

from eahub.base.models import MessagingLog
from eahub.localgroups.models import Organisership
from eahub.tests.cases import EAHubTestCase


class LocalGroupsMessagingTestCase(EAHubTestCase):
    def test_group_messaging(self):
        profile_sender = self.gen.profile()
        localgroup_recipient = self.gen.group()
        profile_organiser = self.gen.profile()
        profile_organiser_2 = self.gen.profile()
        o1 = Organisership(
            user=profile_organiser.user, local_group=localgroup_recipient
        )
        o1.save()

        o2 = Organisership(
            user=profile_organiser_2.user, local_group=localgroup_recipient
        )
        o2.save()

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

        logs = MessagingLog.objects.filter(
            sender_email=profile_sender.user.email
        )

        self.assertEqual(200, response.status_code)
        self.assertIn(message_body, mail.outbox[0].body)
        self.assertEqual("EA Hub <admin@eahub.org>", mail.outbox[0].from_email)
        self.assertIn(profile_organiser.user.email, mail.outbox[0].to[0])
        self.assertIn(profile_organiser_2.user.email, mail.outbox[0].to[0])

        self.assertEqual(1, len(logs))
        self.assertEqual("GROUP", logs[0].recipient_type)
        self.assertIn(profile_organiser.user.email, logs[0].recipient_email)
        self.assertIn(profile_organiser_2.user.email, logs[0].recipient_email)
        self.assertIn(profile_organiser.user.email, logs[0].recipient_email)

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

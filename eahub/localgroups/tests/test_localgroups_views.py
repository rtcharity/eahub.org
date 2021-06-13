from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from eahub.localgroups.models import LocalGroup
from eahub.tests.cases import EAHubTestCase


class GroupViewTestCase(EAHubTestCase):
    def test_group_edit_no_access_to_ordinary_user(self):
        group = self.gen.group()

        profile_visitor = self.gen.profile(is_approved=True)
        self.client.force_login(profile_visitor.user)

        self.assert_post_status_code("localgroups_update", group.slug, 403)
        self.assert_get_status_code("localgroups_update", group.slug, 403)

    def test_group_edit_access_to_organiser(self):
        profile = self.gen.profile(is_approved=True)
        self.client.force_login(profile.user)

        group = self.gen.group(organisers=[profile.user])

        self.assert_post_status_code("localgroups_update", group.slug, 200)
        self.assert_get_status_code("localgroups_update", group.slug, 200)

    def test_group_edit_access_to_staff(self):
        profile = self.gen.profile(is_approved=True)

        content_type = ContentType.objects.get_for_model(LocalGroup)
        permission = Permission.objects.get(
            codename="change_localgroup", content_type=content_type
        )
        profile.user.user_permissions.add(permission)
        self.client.force_login(profile.user)

        group = self.gen.group()

        self.assert_post_status_code("localgroups_update", group.slug, 200)
        self.assert_get_status_code("localgroups_update", group.slug, 200)

    def test_group_delete_not_permitted_for_ordinary_user(self):
        group = self.gen.group()

        profile_visitor = self.gen.profile(is_approved=True)
        self.client.force_login(profile_visitor.user)

        self.assert_post_status_code("localgroups_delete", group.slug, 403)
        self.assert_get_status_code("localgroups_update", group.slug, 403)

    def test_group_delete_permitted_for_organiser(self):
        profile = self.gen.profile(is_approved=True)
        self.client.force_login(profile.user)

        group = self.gen.group(organisers=[profile.user])

        self.assert_post_status_code("localgroups_delete", group.slug, 200)

    def test_group_delete_permitted_for_staff(self):
        profile = self.gen.profile(is_approved=True)

        content_type = ContentType.objects.get_for_model(LocalGroup)
        permission = Permission.objects.get(
            codename="delete_localgroup", content_type=content_type
        )
        profile.user.user_permissions.add(permission)
        self.client.force_login(profile.user)

        group = self.gen.group()

        self.assert_post_status_code("localgroups_delete", group.slug, 200)

    def assert_get_status_code(self, url_name, slug, status_code):
        response_get = self.client.get(reverse(url_name, args=([slug])), follow=True)

        self.assertEqual(response_get.status_code, status_code)

    def assert_post_status_code(self, url_name, slug, status_code):
        response_post = self.client.post(reverse(url_name, args=([slug])), follow=True)

        self.assertEqual(response_post.status_code, status_code)

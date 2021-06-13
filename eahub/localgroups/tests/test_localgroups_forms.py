from eahub.base.models import User
from eahub.localgroups.forms import LocalGroupForm
from eahub.localgroups.models import LocalGroup, Organisership
from eahub.profiles.models import Profile, VisibilityEnum
from eahub.tests.cases import EAHubTestCase


class LocalGroupFormsTestCase(EAHubTestCase):
    def test_organisers_field(self):
        profile_public = self.gen.profile(visibility=VisibilityEnum.PUBLIC)
        profile_internal = self.gen.profile(visibility=VisibilityEnum.INTERNAL)
        profile_private = self.gen.profile(visibility=VisibilityEnum.PRIVATE)

        form = LocalGroupForm(user=profile_public.user)
        organisers_to_choose_from = form.fields["organisers"].queryset

        self.assertCountEqual(
            [profile_public.user, profile_internal.user], organisers_to_choose_from
        )
        self.assertNotIn(profile_private.user, organisers_to_choose_from)

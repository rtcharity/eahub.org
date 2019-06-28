import pytest

from ..localgroups.models import LocalGroup
from ..profiles.models import Profile


# Create two users, and a public and private group: one user organizes both
# groups. Test that each user can see the appropriate groups.
# TODO: Test profile views too.
@pytest.mark.nondestructive
def test_group_visibility(client, django_user_model):
    publicgroup_name = "public-group"
    privategroup_name = "private-group"

    profile1 = Profile.objects.create(user_id=1, name=profile1_name, is_public=True)
    user1 = django_user_model.objects.create(
        profile=profile1, password="testpassone", email="user1@example.com"
    )

    profile2 = Profile.objects.create(user_id=2, name="testusertwo", is_public=True)
    user2 = django_user_model.objects.create(
        profile=profile2, email="user2@example.com"
    )

    group_public = LocalGroup.objects.create(name=publicgroup_name, is_public=True)
    group_public.organisers.set([user1])

    assert group_public.slug == publicgroup_name

    group_private = LocalGroup.objects.create(name=privategroup_name, is_public=False)
    group_private.organisers.set([user1])

    assert profile1.all_organised_groups().count() == 2
    assert profile1.public_organised_groups().count() == 1
    assert profile1.visible_organised_groups(user1).count() == 2
    assert profile1.visible_organised_groups(user2).count() == 1

    response = client.get("/group/%s/" % publicgroup_name)
    assert response.status_code == 200

    response = client.get("/group/%s/" % privategroup_name)
    assert response.status_code == 404

    response = client.get("/groups/")
    assert publicgroup_name in str(response.content)
    assert privategroup_name not in str(response.content)

    client.force_login(user=user1)

    response = client.get("/group/%s/" % publicgroup_name)
    assert response.status_code == 200

    response = client.get("/group/%s/" % privategroup_name)
    assert response.status_code == 200

    response = client.get("/groups/")
    assert publicgroup_name in str(response.content)
    assert privategroup_name in str(response.content)

    client.force_login(user=user2)

    response = client.get("/group/%s/" % publicgroup_name)
    assert response.status_code == 200

    response = client.get("/group/%s/" % privategroup_name)
    assert response.status_code == 404

    response = client.get("/groups/")
    assert publicgroup_name in str(response.content)
    assert privategroup_name not in str(response.content)

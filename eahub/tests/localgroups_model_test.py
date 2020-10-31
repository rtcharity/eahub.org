import pytest
from eahub.localgroups.models import LocalGroup
from eahub.base.models import User

def test_organisers_names():
    localGroup = LocalGroup()
    localGroup.organisers.append(User())

    organisers_names = localGroup.organisers_names()

    assert organisers_names[0] == "User profile missing"
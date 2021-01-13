from authtools import models as authtools_models
from django.db import models


class User(authtools_models.AbstractEmailUser):
    def has_profile(self):
        return hasattr(self, "profile")

from authtools import models as authtools_models


class User(authtools_models.AbstractEmailUser):

    def has_profile(self):
        return hasattr(self, "profile")

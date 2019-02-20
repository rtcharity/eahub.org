from authtools import admin as authtools_admin
from django.contrib import admin

from . import models


admin.site.register(models.User, authtools_admin.UserAdmin)

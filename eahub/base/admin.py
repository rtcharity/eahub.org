from cuser import admin as cuser_admin
from django.contrib import admin

from . import models


admin.site.register(models.User, cuser_admin.UserAdmin)

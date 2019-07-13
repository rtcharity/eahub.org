import os
import environ

env = environ.Env()
base_dir = environ.Path(__file__) - 3


# Core settings: models
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "authtools",
    "captcha",
    "crispy_forms",
    "django_cleanup.apps.CleanupConfig",
    "django_pwned_passwords",
    "rules.apps.AutodiscoverRulesConfig",
    "sorl.thumbnail",
    "eahub.base.apps.BaseConfig",
    "eahub.localgroups.apps.LocalGroupsConfig",
    "eahub.profiles.apps.ProfilesConfig",
    "webpack_loader",
]

# Core settings: security
SECRET_KEY = b"build_secret_key"

# Static files

STATIC_ROOT = "/static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.join(base_dir, "eahub/base/static"),
    os.path.join(base_dir, "eahub/base/dist")
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

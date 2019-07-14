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
    "webpack_loader",
    "eahub.base.apps.BaseConfig",
    "eahub.localgroups.apps.LocalGroupsConfig",
    "eahub.profiles.apps.ProfilesConfig",
]

# Core settings: security
SECRET_KEY = b"build_secret_key"

# Static files
STATIC_ROOT = "/static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = ("/static_build/")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

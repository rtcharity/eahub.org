import environ

env = environ.Env()


# Core settings: models
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "authtools",
    "algoliasearch_django",
    "sekizai",
    "captcha",
    "crispy_forms",
    "django_cleanup.apps.CleanupConfig",
    "django_pwned_passwords",
    "rules.apps.AutodiscoverRulesConfig",
    "sorl.thumbnail",
    "eahub.base.apps.BaseConfig",
    "eahub.localgroups.apps.LocalGroupsConfig",
    "eahub.profiles.apps.ProfilesConfig",
    "import_export",
    "rangefilter",
]

# Core settings: security
SECRET_KEY = b"build_secret_key"

# Static files
STATIC_ROOT = "static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = ("/static_build/",)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALGOLIA = {
    "APPLICATION_ID": env.str("ALGOLIA_APPLICATION_ID", default="PFD0UVG9YB"),
    "API_KEY": env.str("ALGOLIA_API_KEY", default=""),
}

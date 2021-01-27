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
    "django_extensions",
    "rules.apps.AutodiscoverRulesConfig",
    "sorl.thumbnail",
    "import_export",
    "rangefilter",
    "flags",
    "admin_reorder",
    "eahub.base.apps.BaseConfig",
    "eahub.localgroups.apps.LocalGroupsConfig",
    "eahub.profiles.apps.ProfilesConfig",
    "eahub.feedback.apps.FeedbackConfig"
]

# Core settings: security
SECRET_KEY = b"build_secret_key"

# Static files
STATIC_ROOT = "static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = ("/static_build/",)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# search
IS_ENABLE_ALGOLIA = env.str("IS_ENABLE_ALGOLIA", default=True)
ALGOLIA = {
    "APPLICATION_ID": env.str("ALGOLIA_APPLICATION_ID", default="PFD0UVG9YB"),
    "API_KEY": env.str("ALGOLIA_API_KEY", default="d1c9139b2271e35f44a29b12dddb4b06"),
    "API_KEY_READ_ONLY": env.str(
        "API_KEY_READ_ONLY", default="19fd60051efeddf42e707383bf2f15a7"
    ),
    "INDEX_NAME_PROFILES": env.str(
        "ALGOLIA_INDEX_NAME_PROFILES", default="profiles_stage"
    ),
}

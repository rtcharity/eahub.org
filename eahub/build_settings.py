import environ

base_dir = environ.Path(__file__) - 2

# Core settings: models
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "eahub.apps.EahubConfig",
    "profiles",
    "groups",
]

# Core settings: security
SECRET_KEY = b"build_secret_key"

# Static files
STATIC_ROOT = "/static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = [base_dir("eahub/static/")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

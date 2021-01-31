import os
from enum import Enum

import dj_database_url
import environ
import sentry_sdk
from django.core import exceptions
from django.utils.safestring import mark_safe
from dotenv import find_dotenv, load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()
base_dir = environ.Path(__file__) - 3


class DjangoEnv(Enum):
    LOCAL = "local"
    E2E = "e2e"
    STAGE = "stage"
    PROD = "prod"


DJANGO_ENV = env.get_value("DJANGO_ENV", DjangoEnv, default=DjangoEnv.LOCAL)


if DJANGO_ENV == DjangoEnv.LOCAL:
    load_dotenv(find_dotenv(".env"))


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.redirects",
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
    "eahub.base.apps.BaseConfig",
    "eahub.localgroups.apps.LocalGroupsConfig",
    "eahub.profiles.apps.ProfilesConfig",
    "import_export",
    "rangefilter",
    "flags",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django_referrer_policy.middleware.ReferrerPolicyMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]


DATABASES = {
    "default": dj_database_url.parse(
        env.str("DATABASE_URL", "postgres://postgres@postgres:5432/db")
    )
}

DEBUG = env.bool("DEBUG")

vars().update(
    env.email_url(
        "EMAIL_URL",
        backend="django.core.mail.backends.smtp.EmailBackend",
        default="smtp://mail:1025",
    )
)
ADMINS = list(env.dict("ADMINS").items())
DEFAULT_FROM_EMAIL = "EA Hub <admin@eahub.org>"
GROUPS_EMAIL = env.str("GROUPS_EMAIL")
EMAIL_SUBJECT_PREFIX = "[EA Hub] "
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL


if DJANGO_ENV == DjangoEnv.LOCAL:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "cache",
        }
    }
    CACHE_MIDDLEWARE_SECONDS = 60 * 60 * 24
    WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30

    sentry_sdk.init(
        dsn="https://181e4af66382426fb05bd3133031468a@o487305.ingest.sentry.io/5545943",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )


SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

ALLOWED_HOSTS = env.list("HOSTS", default=[]) + ["*"]

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = env.bool(
    "HTTPS",
    default=(DJANGO_ENV == DjangoEnv.PROD or DJANGO_ENV == DjangoEnv.STAGE),
)
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SECRET_KEY = env.str("SECRET_KEY", "development_secret_key")
X_FRAME_OPTIONS = "DENY"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir("eahub/templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "django_settings_export.settings_export",
            ]
        },
    }
]

ROOT_URLCONF = "eahub.config.urls"

# Auth
AUTH_USER_MODEL = "base.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django_pwned_passwords.password_validation.PWNEDPasswordValidator"},
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
]
AUTHENTICATION_BACKENDS = [
    "rules.permissions.ObjectPermissionBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "account_login"
LOGOUT_REDIRECT_URL = "index"
PASSWORD_RESET_TIMEOUT_DAYS = 3

SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

SITE_ID = 1


STATIC_ROOT = os.path.join(base_dir, "static_build/")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    "eahub/base/static/",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


from aldryn_django.storage import parse_storage_url  # noqa: E402,F401; isort:skip

media_config = parse_storage_url(env.str("DEFAULT_STORAGE_DSN"))
DEFAULT_FILE_STORAGE = "aldryn_django.storage.S3MediaStorage"
MEDIA_URL = media_config["MEDIA_URL"]
AWS_MEDIA_ACCESS_KEY_ID = media_config["AWS_MEDIA_ACCESS_KEY_ID"]
AWS_MEDIA_SECRET_ACCESS_KEY = media_config["AWS_MEDIA_SECRET_ACCESS_KEY"]
AWS_MEDIA_STORAGE_BUCKET_NAME = media_config["AWS_MEDIA_STORAGE_BUCKET_NAME"]
AWS_MEDIA_STORAGE_HOST = media_config["AWS_MEDIA_STORAGE_HOST"]
AWS_MEDIA_BUCKET_PREFIX = media_config["AWS_MEDIA_BUCKET_PREFIX"]
AWS_MEDIA_DOMAIN = media_config["AWS_MEDIA_DOMAIN"]


ACCOUNT_ADAPTER = "eahub.base.adapter.EmailBlacklistingAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if SECURE_SSL_REDIRECT else "http"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_FORM_CLASS = "eahub.profiles.forms.SignupForm"
ACCOUNT_USER_DISPLAY = "eahub.base.utils.user_display"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

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

RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_SECRET_KEY", "")
RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_SITE_KEY", "")

# django-crispy-forms
CRISPY_TEMPLATE_PACK = "bootstrap3"

# django-feature-policy
FEATURE_POLICY = {
    "accelerometer": "none",
    "ambient-light-sensor": "none",
    "autoplay": "none",
    "camera": "none",
    "encrypted-media": "none",
    "fullscreen": "none",
    "geolocation": "none",
    "gyroscope": "none",
    "magnetometer": "none",
    "microphone": "none",
    "midi": "none",
    "payment": "none",
    "picture-in-picture": "none",
    "speaker": "none",
    "sync-xhr": "none",
    "usb": "none",
    "vr": "none",
}

PWNED_VALIDATOR_ERROR = mark_safe(
    "For your security, consider using a password that hasn't been "
    "<a target='_blank' href='https://haveibeenpwned.com/passwords'>"
    "involved in a security breach before</a>. "
)
PWNED_VALIDATOR_FAIL_SAFE = False

REFERRER_POLICY = "no-referrer-when-downgrade"

THUMBNAIL_PRESERVE_FORMAT = True

WEBPACK_DEV_URL = env("WEBPACK_DEV_URL", default="http://localhost:8090/assets")

SETTINGS_EXPORT = ["WEBPACK_DEV_URL", "DEBUG", "DJANGO_ENV", "ALGOLIA"]

ADMIN_SITE_HEADER = "EA Hub Staff Portal"
BLACKLISTED_EMAIL_PATTERNS = env.list("BLACKLISTED_EMAIL_PATTERNS", default=[])

LEAN_MANAGERS = list(env.dict("LEAN_MANAGERS").items())
local_groups_airtable_api_key = env.str("LOCAL_GROUPS_AIRTABLE_API_KEY", default=None)
local_groups_airtable_base_key = env.str("LOCAL_GROUPS_AIRTABLE_BASE_KEY", default=None)
if local_groups_airtable_api_key is None and local_groups_airtable_base_key is None:
    LOCAL_GROUPS_AIRTABLE = None
elif (
    local_groups_airtable_api_key is not None
    and local_groups_airtable_base_key is not None
):
    LOCAL_GROUPS_AIRTABLE = {
        "api_key": local_groups_airtable_api_key,
        "base_key": local_groups_airtable_base_key,
    }
else:
    raise exceptions.ImproperlyConfigured(
        "LOCAL_GROUPS_AIRTABLE_API_KEY and LOCAL_GROUPS_AIRTABLE_BASE_KEY must be "
        "provided together"
    )

# feature flags
FLAGS = {
    "MESSAGING_FLAG": [("boolean", env.bool("IS_MESSAGING_ENABLED", default=False))]
}


ADMIN_REORDER = [
    {
        "app": "auth",
        "label": "EAHub",
        "models": [
            {"model": "profiles.Profile", "label": "Profiles"},
            {"model": "localgroups.LocalGroup", "label": "Groups"},
            {"model": "profiles.ProfileAnalyticsLog", "label": "Profile update logs"},
        ],
    },
    {
        "app": "sites",
        "label": "Website administration",
        "models": [
            {"model": "base.User", "label": "User accounts"},
            {"model": "account.EmailAddress", "label": "User account email addresses"},
            {"model": "auth.Group", "label": "Admin permission groups"},
            {"model": "sites.Site", "label": "Domain management & site name"},
            {"model": "redirects.Redirect", "label": "Redirects"},
            {
                "model": "flags.FlagState",
                "label": "Feature flags (beta features) configuration",
            },
        ],
    },
]

from enum import Enum

import dj_database_url
import environ
from django.core import exceptions
from django.utils.safestring import mark_safe
from dotenv import find_dotenv
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


env = environ.Env()
base_dir = environ.Path(__file__) - 3


class DjangoEnv(Enum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


DJANGO_ENV = env.get_value("DJANGO_ENV", DjangoEnv, default=DjangoEnv.LOCAL)


LOCKDOWN_ENABLED = False
LOCKDOWN_PASSWORDS = [
    "staging",
    "demo",
    "test",
    "password",
]

if DJANGO_ENV == DjangoEnv.LOCAL:
    load_dotenv(find_dotenv('.env'))
elif DJANGO_ENV == DjangoEnv.STAGE:
    LOCKDOWN_ENABLED = True


DATABASES = {
    "default": dj_database_url.parse(env.str('DATABASE_URL'))
}

# Core settings: debugging
DEBUG = env.bool("DEBUG")

# Core settings: email
vars().update(
    env.email_url("EMAIL_URL", backend="django.core.mail.backends.smtp.EmailBackend")
)
ADMINS = list(env.dict("ADMINS").items())
DEFAULT_FROM_EMAIL = "EA Hub <admin@eahub.org>"
GROUPS_EMAIL = env.str("GROUPS_EMAIL")
EMAIL_SUBJECT_PREFIX = "[EA Hub] "
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL


if DJANGO_ENV != DjangoEnv.LOCAL:
    sentry_sdk.init(
        dsn="https://4748be7234b54b69966c7a2091ddb26e@o463416.ingest.sentry.io/5468410",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


# Core settings: error reporting
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

# Core settings: globalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Core settings: HTTP
ALLOWED_HOSTS = env.list("HOSTS") + ["127.0.0.1"]
MIDDLEWARE = [
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_referrer_policy.middleware.ReferrerPolicyMiddleware",
    "django_feature_policy.FeaturePolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "applicationinsights.django.ApplicationInsightsMiddleware",
    "lockdown.middleware.LockdownMiddleware",
]
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = env.bool("HTTPS")
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Core settings: logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "appinsights": {
            "level": "WARNING",
            "class": "applicationinsights.django.LoggingHandler",
        },
        "console": {"level": "INFO", "class": "logging.StreamHandler"},
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["appinsights", "console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "eahub": {
            "handlers": ["appinsights", "console", "mail_admins"],
            "level": "INFO",
        },
    },
}

# Core settings: models
from .build_settings import INSTALLED_APPS  # noqa: E402,F401; isort:skip

# Core settings: security
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SECRET_KEY = env.bytes("SECRET_KEY")
X_FRAME_OPTIONS = "DENY"

# Core settings: templates
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

# Core settings: URLs
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

# Sessions
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# Sites
SITE_ID = 1

# Static files
if DJANGO_ENV == DjangoEnv.PROD:
    from .build_settings import STATICFILES_DIRS
else:
    from .build_settings_dev import STATICFILES_DIRS  # noqa: F401,F402; isort:skip

from .build_settings import (  # noqa: E402,F401; isort:skip
    STATICFILES_STORAGE,
    STATIC_ROOT,
    STATIC_URL,
)

# Application Insights
APPLICATION_INSIGHTS = {
    "ikey": env.str("APPLICATION_INSIGHTS_INSTRUMENTATION_KEY", default=None)
}



from aldryn_django.storage import parse_storage_url
media_config = parse_storage_url(env.str('DEFAULT_STORAGE_DSN'))
DEFAULT_FILE_STORAGE = 'aldryn_django.storage.S3MediaStorage'
MEDIA_URL = media_config['MEDIA_URL']
AWS_MEDIA_ACCESS_KEY_ID = media_config['AWS_MEDIA_ACCESS_KEY_ID']
AWS_MEDIA_SECRET_ACCESS_KEY = media_config['AWS_MEDIA_SECRET_ACCESS_KEY']
AWS_MEDIA_STORAGE_BUCKET_NAME = media_config['AWS_MEDIA_STORAGE_BUCKET_NAME']
AWS_MEDIA_STORAGE_HOST = media_config['AWS_MEDIA_STORAGE_HOST']
AWS_MEDIA_BUCKET_PREFIX = media_config['AWS_MEDIA_BUCKET_PREFIX']
AWS_MEDIA_DOMAIN = media_config['AWS_MEDIA_DOMAIN']


# allauth
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

# search
ALGOLIA = {
    "APPLICATION_ID": env.str("ALGOLIA_APPLICATION_ID", default="PFD0UVG9YB"),
    "API_KEY": env.str("ALGOLIA_API_KEY", default=""),
}

# Django reCAPTCHA
recaptcha_v3_secret_key = env.str("RECAPTCHA_V3_SECRET_KEY", default=None)
recaptcha_v3_site_key = env.str("RECAPTCHA_V3_SITE_KEY", default=None)
if recaptcha_v3_secret_key is not None and recaptcha_v3_site_key is not None:
    RECAPTCHA_PRIVATE_KEY = recaptcha_v3_secret_key
    RECAPTCHA_PUBLIC_KEY = recaptcha_v3_site_key
    RECAPTCHA_REQUIRED_SCORE = 0.85
elif recaptcha_v3_secret_key is not None or recaptcha_v3_site_key is not None:
    raise exceptions.ImproperlyConfigured(
        "RECAPTCHA_V3_SECRET_KEY and RECAPTCHA_V3_SITE_KEY must be provided together"
    )

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

# Django PWNED Passwords
PWNED_VALIDATOR_ERROR = mark_safe(
    "For your security, consider using a password that hasn't been "
    "<a target='_blank' href='https://haveibeenpwned.com/passwords'>"
    "involved in a security breach before</a>. "
)
PWNED_VALIDATOR_FAIL_SAFE = False

# django-referrer-policy
REFERRER_POLICY = "no-referrer-when-downgrade"

# sorl-thumbnail
THUMBNAIL_PRESERVE_FORMAT = True

WEBPACK_DEV_URL = env("WEBPACK_DEV_URL", default="http://localhost:8090/assets")

SETTINGS_EXPORT = [
    "WEBPACK_DEV_URL",
    "DEBUG",
    "DJANGO_ENV",
    "ALGOLIA",
]

# EA Hub
ADMIN_SITE_HEADER = "EA Hub Staff Portal"
BLACKLISTED_EMAIL_PATTERNS = env.list("BLACKLISTED_EMAIL_PATTERNS", default=[])

# Local groups
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

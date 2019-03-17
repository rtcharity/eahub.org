from django.core import exceptions
import environ

env = environ.Env()
base_dir = environ.Path(__file__) - 3

# Core settings: cache
CACHES = {
    "default": env.cache_url("CACHE_URL", backend="django_redis.cache.RedisCache")
}

# Core settings: database
DATABASES = {
    "default": env.db_url("DATABASE_URL", engine="django.db.backends.postgresql")
}
if "LEGACY_DATABASE_URL" in env:
    DATABASES["legacy"] = env.db_url(
        "LEGACY_DATABASE_URL", engine="django.db.backends.mysql"
    )

# Core settings: debugging
DEBUG = env.bool("DEBUG")

# Core settings: email
vars().update(
    env.email_url("EMAIL_URL", backend="django.core.mail.backends.smtp.EmailBackend")
)
ADMINS = list(env.dict("ADMINS").items())
DEFAULT_FROM_EMAIL = "EA Hub <noreply@eahub.org>"
EMAIL_SUBJECT_PREFIX = "[EA Hub] "
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Core settings: file uploads
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"

# Core settings: globalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Core settings: HTTP
ALLOWED_HOSTS = env.list("HOSTS") + ["127.0.0.1"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "eahub.base.middleware.BrokenLinkEmailsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "applicationinsights.django.ApplicationInsightsMiddleware",
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
from .build_settings import INSTALLED_APPS

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
            ]
        },
    }
]

# Core settings: URLs
ROOT_URLCONF = "eahub.config.urls"

# Auth
AUTH_USER_MODEL = "base.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTHENTICATION_BACKENDS = [
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
]
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "/profile/login/"
LOGOUT_REDIRECT_URL = "index"

# Sessions
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# Static files
from .build_settings import STATIC_ROOT, STATIC_URL, STATICFILES_STORAGE

# Application Insights
APPLICATION_INSIGHTS = {
    "ikey": env.str("APPLICATION_INSIGHTS_INSTRUMENTATION_KEY", default=None)
}

# django-storages
AZURE_CONNECTION_STRING = env.str("AZURE_CONNECTION_STRING")
AZURE_CONTAINER = env.str("AZURE_CONTAINER")
AZURE_SSL = SECURE_SSL_REDIRECT
AZURE_URL_EXPIRATION_SECS = 3600

# sorl-thumbnail
THUMBNAIL_PRESERVE_FORMAT = True

# EA Hub
ADMIN_SITE_HEADER = "EA Hub Staff Portal"

# Profiles
RECAPTCHA_SECRET_KEY = env.str("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = env.str("RECAPTCHA_SITE_KEY")

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
        "LOCAL_GROUPS_AIRTABLE_API_KEY and LOCAL_GROUPS_AIRTABLE_BASE_KEY must be provided together"
    )

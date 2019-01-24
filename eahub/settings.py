import environ

env = environ.Env()
base_dir = environ.Path(__file__) - 2

# Core settings: cache
CACHES = {
    "default": env.cache_url("CACHE_URL", backend="django_redis.cache.RedisCache")
}

# Core settings: database
DATABASES = {
    "default": env.db_url("DATABASE_URL", engine="django.db.backends.postgresql")
}

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
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# Core settings: globalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Core settings: HTTP
ALLOWED_HOSTS = env.list("HOSTS")
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = env.bool('HTTPS')
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Core settings: models
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "eahub.apps.EahubConfig",
    "groups",
    "profiles",
]

# Core settings: security
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
SECRET_KEY = env.bytes("SECRET_KEY")
X_FRAME_OPTIONS = "DENY"

# Core settings: templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [base_dir("templates/")],
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
ROOT_URLCONF = "eahub.urls"

# Auth
AUTH_USER_MODEL = "profiles.Profile"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGIN_REDIRECT_URL = "index"
LOGIN_URL = "/profile/login/"
LOGOUT_REDIRECT_URL = "index"

# Sessions
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Static files
STATIC_ROOT = base_dir("staticfiles/")
STATIC_URL = "/static/"
STATICFILES_DIRS = [base_dir("eahub/static/"), base_dir("static/")]

# django-storages
AZURE_CONNECTION_STRING = env.str('AZURE_CONNECTION_STRING')
AZURE_CONTAINER = env.str('AZURE_CONTAINER')
AZURE_SSL = SECURE_SSL_REDIRECT
AZURE_URL_EXPIRATION_SECS = 3600

# EA Hub
ADMIN_SITE_HEADER = "EA Hub Staff Portal"

# Profiles
RECAPTCHA_SECRET_KEY = env.str("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = env.str("RECAPTCHA_SITE_KEY")

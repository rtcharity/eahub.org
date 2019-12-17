# Core settings: models
from .build_settings import INSTALLED_APPS  # noqa: F401; isort:skip

from .build_settings import (  # noqa: F401; isort:skip
    SECRET_KEY,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_STORAGE,
)

# Static files
STATICFILES_DIRS = ("/eahub/base/static/",)

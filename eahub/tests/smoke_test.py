import pytest
from django.test import override_settings


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
@pytest.mark.nondestructive
def test_homepage_title(driver, live_server):
    driver.get(live_server.url)
    assert driver.title == "Effective Altruism Hub • Home"

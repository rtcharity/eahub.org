import pytest


@pytest.mark.nondestructive
def test_homepage_title(driver, live_server):
    driver.get(live_server.url)
    assert driver.title == "EA Hub Home"

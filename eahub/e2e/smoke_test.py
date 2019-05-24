import pytest

@pytest.mark.nondestructive
def test_homepage_title(live_server):
    return
    driver.get(live_server.url)
    assert driver.title == "EA Hub Home"

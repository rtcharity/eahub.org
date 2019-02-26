import pytest

@pytest.mark.nondestructive
def test_homepage_title(driver, base_url):
    driver.get(base_url)
    assert driver.title == "EA Hub Home"

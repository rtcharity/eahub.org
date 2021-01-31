import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from eahub.config.settings import DjangoEnv


@override_settings(
    DJANGO_ENV=DjangoEnv.E2E,
)
class E2ETestCase(StaticLiveServerTestCase):
    host = "0.0.0.0"
    port = 8000

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def find(self, selector: str) -> WebElement:
        # find_element_by_css_selector doesn't work in docker, but works outside of docker
        return self.selenium.find_element(By.CSS_SELECTOR, selector)

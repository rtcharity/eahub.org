import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from eahub.config.settings import DjangoEnv


@override_settings(
    DJANGO_ENV=DjangoEnv.E2E,
)
@tag("e2e")
class E2ETestCase(StaticLiveServerTestCase):
    cls.host = "0.0.0.0"
    cls.port = 8000

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            options=webdriver.ChromeOptions()
        )

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def find(self, selector: str) -> WebElement:
        # find_element_by_css_selector doesn't work in docker, but works outside
        return self.selenium.find_element(By.CSS_SELECTOR, selector)

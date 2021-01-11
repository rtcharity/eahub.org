import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'


class SignUpTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '0.0.0.0'
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_visit_site(self):
        self.selenium.get("https://google.com")
        print(self.selenium.title)

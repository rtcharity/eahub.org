import os
import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'


class SignUpTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = '0.0.0.0'
        super().setUpClass()

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()

    def test_visit_site(self):
        print("in test")
        selenium = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        print("get sel")
        selenium.get("google.com")
        print("in test 2")
        print(selenium.title)
        selenium.quit()

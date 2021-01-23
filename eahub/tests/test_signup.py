import socket

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By

from eahub.base.models import User


class SignUpTest(StaticLiveServerTestCase):
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

    def test_visit_site(self):
        email = "test@eahub.org"
        password = "Wa4@;fh>A/~W#6SH"

        self.selenium.get(self.live_server_url)

        self.selenium.find_element(By.CSS_SELECTOR, "#navbar_signup").click()

        self.selenium.find_element(By.CSS_SELECTOR, "#id_name").send_keys("Test User")
        self.selenium.find_element(By.CSS_SELECTOR, "#id_email").send_keys(email)
        self.selenium.find_element(By.CSS_SELECTOR, "#id_password1").send_keys(password)
        self.selenium.find_element(By.CSS_SELECTOR, "#id_password2").send_keys(password)
        self.selenium.find_element(By.CSS_SELECTOR, "#id_is_public").click()

        self.selenium.find_element(By.CSS_SELECTOR, "#submit").click()

        self.selenium.find_element(By.CSS_SELECTOR, ".profile-welcome")

        User.objects.get(email=email)

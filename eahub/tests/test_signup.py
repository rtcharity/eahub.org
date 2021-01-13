import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By


class SignUpTest(StaticLiveServerTestCase):
    host = '0.0.0.0'
    port = 8000
    
    @classmethod
    def setUpClass(cls):
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
        signup_button = "#navbar_signup"
        name_field = "#id_name"
        email_field = "#id_email"
        password_field_1 = "#id_password1"
        password_field_2 = "#id_password2"
        public = "#id_is_public"
        submit = "#submit"
    
        name = "TestUser"
        email = "test@eahub.org"
        password = "Wa4@;fh>A/~W#6SH"
    
        # When:
        print('get')
        self.selenium.get(f'http://0.0.0.0/')
        print('get after')
    
        # All fields filled in
        self.selenium.find_element(By.CSS_SELECTOR, signup_button).click()
        self.selenium.find_element(By.CSS_SELECTOR, name_field).send_keys(name)
        self.selenium.find_element(By.CSS_SELECTOR, email_field).send_keys(email)
        self.selenium.find_element(By.CSS_SELECTOR, password_field_1).send_keys(password)
        self.selenium.find_element(By.CSS_SELECTOR, password_field_2).send_keys(password)
    
        # "Visible to public" unchecked
        self.selenium.find_element(By.CSS_SELECTOR, public).click()
    
        # Then:
        # Submit
        self.selenium.find_element(By.CSS_SELECTOR, submit).click()
        time.sleep(10)

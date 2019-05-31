import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.nondestructive
def test_signup_success(driver, live_server):
    signup_button = '#navbar_signup'
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
    driver.get(live_server.url)

    # All fields filled in
    driver.find_element(By.CSS_SELECTOR, signup_button).click()
    driver.find_element(By.CSS_SELECTOR, name_field).send_keys(name)
    driver.find_element(By.CSS_SELECTOR, email_field).send_keys(email)
    driver.find_element(By.CSS_SELECTOR, password_field_1).send_keys(password)
    driver.find_element(By.CSS_SELECTOR, password_field_2).send_keys(password)

    # "Visible to public" unchecked
    driver.find_element(By.CSS_SELECTOR, public).click()

    # Recaptcha solved
    driver.find_element(By.CSS_SELECTOR, password_field_2).send_keys(Keys.TAB + Keys.TAB + Keys.SPACE)
    time.sleep(5)

    # Then:
    # Submit
    driver.find_element(By.CSS_SELECTOR, submit).click()
    time.sleep(10)

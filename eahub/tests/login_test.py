from selenium.webdriver.common.by import By
import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.nondestructive
def test_login_failure(driver, live_server):
    # Given
    actions = webdriver.ActionChains(driver)

    login_field = "#id_login"
    password_field = "#id_password"
    login = "test@test.te"
    password = "QnnTe=w{LkG=6Zc"
    login_button = "#submit"

    # When
    driver.get(live_server.url)
    driver.find_element(By.CSS_SELECTOR, "#navbar_login").click()

    actions.move_to_element(driver.find_element(By.CSS_SELECTOR, login_field)).send_keys(login)
    actions.move_to_element(driver.find_element(By.CSS_SELECTOR, password_field)).click().send_keys(password) \
        .perform()

    driver.find_element(By.CSS_SELECTOR, login_button).click()

    # Then
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of(driver.find_element(By.CSS_SELECTOR, "#login-danger")))
    except TimeoutException:
        pytest.fail("Expected element not located")


@pytest.mark.nondestructive
def test_login_success(driver, live_server):
    # TODO Implement scenario: successful login
    pass

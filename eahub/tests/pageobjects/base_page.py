from selenium import webdriver
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

    def visit(self, url):
        self.driver.get(url)

    def find_element(self, locator_strategy, locator):
        return self.driver.find_element(locator_strategy, locator)

    def find_elements(self, locator_strategy, locator):
        return self.driver.find_elements(locator_strategy, locator)

    def click_element(self, locator_strategy, locator):
        self.wait_for_element(locator_strategy, locator)
        self.find_element(locator_strategy, locator).click()

    def click_element_javascript(self, selector):
        self.driver.execute_script("""document.querySelector("%s").click();""" % selector)

    def get_text(self, locator_strategy, locator):
        return (self.find_element(locator_strategy, locator)).get_attribute("innerText")

    def verify_title(self):
        return self.driver.title()

    def wait_for_title_to_be(self, expected_title):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.title_is(expected_title))
        except TimeoutException:
            print("Title did not match expected title")

    def wait_for_element(self, locator_strategy, locator):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((locator_strategy, locator)))
        except TimeoutException:
            print("Locator %s did not appear in X seconds" % locator)

    def wait_for_element_to_be_visible(self, locator_strategy, locator):
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((locator_strategy, locator)))
        except TimeoutException:
            print("Element %s not visible" % locator)

    def wait_until_element_dissapear(self, locator_strategy, locator):
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.invisibility_of_element_located(
                (locator_strategy, locator)))
        except TimeoutException:
            print("Element %s was still visible" % locator)

    def wait_until_element_clickable(self, locator_strategy, locator):
        try:
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.element_to_be_clickable(
                (locator_strategy, locator)))
        except TimeoutException:
            print("Element %s was still visible" % locator)

    def select_value_from_dropdown(self, value_to_select, locator_strategy):
        select = Select(self.find_element(*locator_strategy))
        select.select_by_value(value_to_select)

    def select_by_inner_text(self, text_to_select, locator_strategy, contains=False):
        for result in self.find_elements(*locator_strategy):
            if contains:
                if text_to_select in result.get_attribute("innerText"):
                    result.click()
                    return True
            if result.get_attribute("innerText") == text_to_select:
                result.click()
                return True
        return False

    def action_chains_send_keys(self, key_to_send, locator_strategy):
        element = self.find_element(*locator_strategy)
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element).click().send_keys(key_to_send).perform()

    def switch_to_frame(self, frame_name):
        try:
            self.driver.switch_to_frame(frame_name)
        except NoSuchFrameException:
            print("Failed while switching to frame %s" % frame_name)

    def switch_back_from_frame(self):
        self.driver.switch_to_default_content()

    def quit(self):
        self.driver.quit()
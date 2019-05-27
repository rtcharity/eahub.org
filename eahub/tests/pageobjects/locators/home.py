from selenium.webdriver.common.by import By


class Home(object):
    BANNER = (By.CSS_SELECTOR, '#body > div.jumbotron > div > img')
    BUTTON_PROFILES = (By.CSS_SELECTOR, '#profiles')
    BUTTON_GROUPS = (By.CSS_SELECTOR, '#groups')
    BUTTON_RESOURCES = (By.CSS_SELECTOR, '#resoures')
    BUTTON_DONATION_SWAP = (By.CSS_SELECTOR, '#donation_swap')
    BUTTON_ABOUT = (By.CSS_SELECTOR, '#about')
    BUTTON_FEEDBACK = (By.CSS_SELECTOR, '#feedback')
    MAP = (By.CSS_SELECTOR, '#map')
    MAP_SELECTOR_GROUPS = (By.CSS_SELECTOR, '#map_selector_groups')
    MAP_SELECTOR_INDIVIDUALS = (By.CSS_SELECTOR, '#map_selector_ind')
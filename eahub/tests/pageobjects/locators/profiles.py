from selenium.webdriver.common.by import By


class Profiles(object):
    PROFILES_MAP = (By.CSS_SELECTOR, '#map')
    BUTTON_SIGNUP = (By.CSS_SELECTOR, '#profiles_signup')
    BUTTON_PROFILE = (By.CSS_SELECTOR, '#profiles_view')
    BUTTON_CONTACT = (By.CSS_SELECTOR, '#profiles_contact')
    FILTERBOX = (By.CSS_SELECTOR, '#filterbox')
    SORT_DESC_NAME = (By.CSS_SELECTOR, '#datatable-groups > thead > tr > th.sorting_desc')
    SORT_ASC_NAME = (By.CSS_SELECTOR, '#datatable-groups > thead > tr > th.sorting_asc')
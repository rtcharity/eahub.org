from selenium.webdriver.common.by import By


class Groups(object):
    GROUPS_MAP = (By.CSS_SELECTOR, '#map')
    BUTTON_CREATE = (By.CSS_SELECTOR, '#groups_create')
    BUTTON_RESOURCES = (By.CSS_SELECTOR, '#groups_resources')
    BUTTON_CONTACT = (By.CSS_SELECTOR, '#groups_contact')
    FILTERBOX = (By.CSS_SELECTOR, '#filterbox')
    SORT_DESC_NAME = (By.CSS_SELECTOR, '#datatable-groups > thead > tr > th.sorting_desc')
    SORT_ASC_NAME = (By.CSS_SELECTOR, '#datatable-groups > thead > tr > th.sorting_asc')
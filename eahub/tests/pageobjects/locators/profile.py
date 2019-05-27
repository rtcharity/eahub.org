from selenium.webdriver.common.by import By


class Profile(object):
    PROFILE_PICTURE = (By.CSS_SELECTOR, '#body > div.container.animated > div > div.col-xs-12.col-md-3 > img')
    PROFILE_NAME = (By.CSS_SELECTOR, '#body > div.container.animated > div > div.col-xs-12.col-md-6 > h1')
    PROFILE_EDIT = (By.CSS_SELECTOR, '#account_edit_profile')
    PROFILE_CHANGE_EMAIL = (By.CSS_SELECTOR, '#account_change_email')
    PROFILE_CHANGE_PASSWORD = (By.CSS_SELECTOR, '#account_change_password')
    PROFILE_DOWNLOAD_DATA = (By.CSS_SELECTOR, '#profile_download')
    PROFILE_DELETE = (By.CSS_SELECTOR, '#profile_delete')
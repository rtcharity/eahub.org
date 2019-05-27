from selenium.webdriver.common.by import By


class TopNavBar(object):
    LOGO = (By.CSS_SELECTOR, '#logo')
    BUTTON_LOGIN = (By.CSS_SELECTOR, '#login')
    BUTTON_SIGNUP = (By.CSS_SELECTOR, '#signup')
    BUTTON_PROFILE = (By.CSS_SELECTOR, '#myprofile')
    BUTTON_LOGOUT = (By.CSS_SELECTOR, '#logout')
    BUTTON_BURGER = (By.CSS_SELECTOR, '#burger-btn')
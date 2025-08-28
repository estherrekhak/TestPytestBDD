from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.popup_handler import close_unwanted_popups

class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, 'first-name')
    LAST_NAME_INPUT = (By.ID, 'last-name')
    POSTAL_CODE_INPUT = (By.ID, 'postal-code')
    CONTINUE_BUTTON = (By.ID, 'continue')

    def fill_checkout_info(self, first_name, last_name, postal_code):
        close_unwanted_popups(self.driver)
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.popup_handler import close_unwanted_popups

class ConfirmationPage(BasePage):
    FINISH_BUTTON = (By.ID, 'finish')
    CONFIRMATION_TEXT = (By.CLASS_NAME, 'complete-header')

    def finish_checkout(self):
        close_unwanted_popups(self.driver)
        print(f"DEBUG: URL before clicking finish: {self.driver.current_url}")
        print(f"DEBUG: Page source before clicking finish: {self.driver.page_source[:500]}")
        self.click(self.FINISH_BUTTON)

    def get_confirmation_text(self):
        return self.find_element(self.CONFIRMATION_TEXT).text

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.popup_handler import close_unwanted_popups

class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.ID, 'checkout')  # If this fails, try 'checkout'

    def click_checkout(self):
        print(f"DEBUG: Attempting to click checkout button with locator: {self.CHECKOUT_BUTTON}")
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        close_unwanted_popups(self.driver)
        checkout_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.driver.execute_script("arguments[0].click();", checkout_btn)
        import time
        for _ in range(10):
            if '/checkout-step-one' in self.driver.current_url:
                break
            time.sleep(1)
        print(f"DEBUG: URL after clicking checkout button: {self.driver.current_url}")

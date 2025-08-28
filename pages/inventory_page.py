from selenium.webdriver.common.by import By
from .base_page import BasePage

class InventoryPage(BasePage):
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@id,'add-to-cart')]")
    CART_ICON = (By.XPATH, "//a[@class='shopping_cart_link']")

    def add_item_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def go_to_cart(self):
        from utils.popup_handler import close_unwanted_popups
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        print(f"DEBUG: Waiting for cart icon to be clickable: {self.CART_ICON}")
        close_unwanted_popups(self.driver)
        cart_icon = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.CART_ICON))
        self.driver.execute_script("arguments[0].click();", cart_icon)
        import time
        for _ in range(10):
            if '/cart' in self.driver.current_url:
                break
            time.sleep(1)
        print(f"DEBUG: URL after clicking cart icon: {self.driver.current_url}")

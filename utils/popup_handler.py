from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def close_unwanted_popups(driver, timeout=2):
    try:
        popup = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'OK') or contains(text(), '×') or @class='popup-close']")
            )
        )
        popup.click()
        print("Popup closed")
    except TimeoutException:
        pass  # No popup appeared

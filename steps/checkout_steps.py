import allure
from pytest_bdd import given, when, then, scenarios
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.confirmation_page import ConfirmationPage

# Link this step file to the checkout.feature file
scenarios('../features/checkout.feature')

# =====================
# Step Definitions for: checkout.feature
# =====================

@given('the user has items in the cart')
def user_has_items_in_cart(browser, browser_type):
    """
    Step: Given the user has items in the cart
    Feature: Checkout process
    Maps to: checkout.feature: Given the user has items in the cart
    """
    browser.get('https://www.saucedemo.com/')
    login_page = LoginPage(browser)
    login_page.login('standard_user', 'secret_sauce')
    inventory_page = InventoryPage(browser)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()

@when('the user completes the checkout process')
def complete_checkout_process(browser, browser_type):
    """
    Step: When the user completes the checkout process
    Feature: Checkout process
    Maps to: checkout.feature: When the user completes the checkout process
    """
    cart_page = CartPage(browser)
    cart_page.click_checkout()
    print(f"DEBUG: URL after clicking checkout: {browser.current_url}")
    from utils.popup_handler import close_unwanted_popups
    close_unwanted_popups(browser)
    checkout_page = CheckoutPage(browser)
    print(f"DEBUG: Page source at checkout: {browser.page_source[:500]}")
    checkout_page.fill_checkout_info('John', 'Doe', '12345')
    # Wait for navigation to next step (overview page) before clicking Finish
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, 'finish'))
        )
        print(f"DEBUG: Arrived at overview page, ready to click Finish. URL: {browser.current_url}")
    except Exception as e:
        print(f"ERROR: Did not reach overview page: {e}")
        print(f"DEBUG: Current URL: {browser.current_url}")
        print(f"DEBUG: Page source: {browser.page_source[:1000]}")
        raise
    confirmation_page = ConfirmationPage(browser)
    confirmation_page.finish_checkout()

@then('the user should see the confirmation page')
def user_sees_confirmation_page(browser, browser_type):
    """
    Step: Then the user should see the confirmation page
    Feature: Checkout process
    Maps to: checkout.feature: Then the user should see the confirmation page
    """
    confirmation_page = ConfirmationPage(browser)
    actual_text = confirmation_page.get_confirmation_text()
    # Capture screenshot and attach to Allure
    screenshot = browser.get_screenshot_as_png()
    allure.attach(screenshot, name="Confirmation Screenshot", attachment_type=allure.attachment_type.PNG)
    print(f"DEBUG: Confirmation text: {actual_text}")
    assert 'Thank you for your order!' in actual_text

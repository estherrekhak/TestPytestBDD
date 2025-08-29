
from pytest_bdd import given, when, then, scenarios
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Link this step file to the login.feature file
scenarios('../features/login.feature')

# =====================
# Step Definitions for: login.feature
# =====================

@given('the user is on the login page')
def user_on_login_page(browser, browser_type):
    print(f"STEP: user_on_login_page in {browser_type}")
    """
    Step: Given the user is on the login page
    Feature: Login functionality
    Maps to: login.feature: Given the user is on the login page
    """
    browser.get('https://www.saucedemo.com/')

@when('the user enters valid credentials')
def enter_valid_credentials(browser, browser_type):
    print(f"STEP: enter_valid_credentials in {browser_type}")
    """
    Step: When the user enters valid credentials
    Feature: Login functionality
    Maps to: login.feature: When the user enters valid credentials
    """
    login_page = LoginPage(browser)
    login_page.login('standard_user', 'secret_sauce')

@then('the user should be redirected to the inventory page')
def redirected_to_inventory(browser, browser_type):
    print(f"STEP: redirected_to_inventory in {browser_type}")
    """
    Step: Then the user should be redirected to the inventory page
    Feature: Login functionality
    Maps to: login.feature: Then the user should be redirected to the inventory page
    """
    inventory_page = InventoryPage(browser)
    assert 'inventory' in browser.current_url

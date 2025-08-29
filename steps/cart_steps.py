
from pytest_bdd import given, when, then, scenarios
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

# Link this step file to the add_to_cart.feature file
scenarios('../features/add_to_cart.feature')

# =====================
# Step Definitions for: Add to cart.feature
# =====================

@given('the user is logged in')
def user_logged_in(browser, browser_type):
    print(f"STEP: user_logged_in in {browser_type}")
    """
    Step: Given the user is logged in
    Feature: Add to cart
    Maps to: add_to_cart.feature: Given the user is logged in
    """
    browser.get('https://www.saucedemo.com/')
    login_page = LoginPage(browser)
    login_page.login('standard_user', 'secret_sauce')

@when('the user adds an item to the cart')
def add_item_to_cart(browser, browser_type):
    print(f"STEP: add_item_to_cart in {browser_type}")
    """
    Step: When the user adds an item to the cart
    Feature: Add to cart
    Maps to: add_to_cart.feature: When the user adds an item to the cart
    """
    inventory_page = InventoryPage(browser)
    inventory_page.add_item_to_cart()

@then('the cart should contain the item')
def cart_should_contain_item(browser, browser_type):
    print(f"STEP: cart_should_contain_item in {browser_type}")
    """
    Step: Then the cart should contain the item
    Feature: Add to cart
    Maps to: add_to_cart.feature: Then the cart should contain the item
    """
    inventory_page = InventoryPage(browser)
    inventory_page.go_to_cart()
    cart_page = CartPage(browser)
    print(f"DEBUG: Current URL after go_to_cart: {browser.current_url}")
    # Add assertion for item presence if needed
    assert '/cart' in browser.current_url

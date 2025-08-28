__feature__ = '../features/add_to_cart.feature'
import pytest
from steps.cart_steps import *
from pytest_bdd import scenarios

# Dynamically select feature file based on --featurefiles option
import os
def get_feature_file():
    import pytest
    featurefiles = pytest.config.getoption("featurefiles") if hasattr(pytest, 'config') else None
    if featurefiles:
        for f in featurefiles:
            if os.path.basename(f) == 'add_to_cart.feature':
                return f
    return '../features/add_to_cart.feature'

scenarios(get_feature_file())

def test_add_item_to_cart(browser, browser_type):
    user_logged_in(browser, browser_type)
    add_item_to_cart(browser, browser_type)
    cart_should_contain_item(browser, browser_type)

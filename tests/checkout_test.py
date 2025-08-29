
__feature__ = '../features/checkout.feature'
import pytest
from steps.checkout_steps import *
from pytest_bdd import scenarios

# Dynamically select feature file based on --featurefiles option
import os
def get_feature_file():
    import pytest
    featurefiles = pytest.config.getoption("featurefiles") if hasattr(pytest, 'config') else None
    if featurefiles:
        for f in featurefiles:
            if os.path.basename(f) == 'checkout.feature':
                return f
    return '../features/checkout.feature'

scenarios(get_feature_file())

def test_successful_checkout(browser, browser_type):
    user_has_items_in_cart(browser, browser_type)
    complete_checkout_process(browser, browser_type)
    user_sees_confirmation_page(browser, browser_type)

__feature__ = '../features/login.feature'
import pytest
from steps.login_steps import *
from pytest_bdd import scenarios

# Dynamically select feature file based on --featurefiles option
import os
def get_feature_file():
    import pytest
    featurefiles = pytest.config.getoption("featurefiles") if hasattr(pytest, 'config') else None
    if featurefiles:
        for f in featurefiles:
            if os.path.basename(f) == 'login.feature':
                return f
    return '../features/login.feature'

scenarios(get_feature_file())

def test_successful_login(browser, browser_type):
    user_on_login_page(browser, browser_type)
    enter_valid_credentials(browser, browser_type)
    redirected_to_inventory(browser, browser_type)


import os
import pytest
from steps.cart_steps import *
from pytest_bdd import scenarios

feature_file = os.getenv("FEATUREFILES", "../features/add_to_cart.feature").split(",")[0]
if not feature_file.startswith("../"):
    feature_file = os.path.join("..", feature_file)

import pytest

import pytest

import pytest

import pytest

def test_add_item_to_cart(browser, browser_type):
    from pytest_bdd import scenarios
    scenarios(feature_file)

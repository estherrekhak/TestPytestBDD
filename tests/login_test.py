__feature__ = '../features/login.feature'
import os
import pytest
from steps.login_steps import *
from pytest_bdd import scenarios

feature_file = os.getenv("FEATUREFILES", "../features/login.feature").split(",")[1] if len(os.getenv("FEATUREFILES", "").split(",")) > 1 else "../features/login.feature"
if not feature_file.startswith("../"):
    feature_file = os.path.join("..", feature_file)

import pytest

import pytest

import pytest

import pytest

def test_successful_login(browser, browser_type):
    from pytest_bdd import scenarios
    scenarios(feature_file)

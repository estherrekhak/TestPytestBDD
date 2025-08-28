import pytest
from selenium import webdriver
import allure
import os


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="append",
        default=["chrome"],
        help="Browser(s) to run tests against: chrome, edge. Can be specified multiple times."
    )
    parser.addoption(
        "--tags",
        action="store",
        default=None,
        help="Run only scenarios with the given tag (e.g. --tags=smoke)"
    )
    parser.addoption(
        "--featurefiles",
        action="append",
        default=None,
        help="Feature file(s) to run (e.g. --featurefiles=features/add_to_cart.feature). Can be specified multiple times."
    )

@pytest.fixture
def browser(request, browser_type):
    # Use browser_type from test parameter for correct parallel execution
    if browser_type == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--disable-automation-extension")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_type == "edge":
        from selenium.webdriver.edge.options import Options as EdgeOptions
        edge_options = EdgeOptions()
        edge_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })
        edge_options.add_argument("--inprivate")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-save-password-bubble")
        edge_options.add_argument("--disable-automation-extension")
        edge_options.add_argument("--disable-infobars")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option("useAutomationExtension", False)
        driver = webdriver.Edge(options=edge_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")
    yield driver
    driver.quit()

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames:
        browsers = metafunc.config.getoption("browser")
        metafunc.parametrize("browser_type", browsers, scope="function")

    # Optional: filter tests by feature files at runtime
    featurefiles = metafunc.config.getoption("featurefiles")
    if featurefiles:
        # Support comma-separated and multiple --featurefiles values
        import os
        normalized = []
        for f in featurefiles:
            normalized.extend([os.path.basename(x.strip()) for x in f.split(",") if x.strip()])
        # Only run tests whose feature file matches the selected featurefiles
        scenario_feature = getattr(metafunc.module, "__feature__", None)
        if scenario_feature and os.path.basename(scenario_feature) not in normalized:
            import pytest
            pytest.skip(f"Skipping test: feature file {scenario_feature} not selected.")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # Only add screenshot for actual failing test calls
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser", None)
        if browser:
            screenshot_dir = os.path.join(os.getcwd(), "allure_screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            try:
                browser.save_screenshot(screenshot_path)
                allure.attach.file(screenshot_path, name=f"Screenshot_{item.name}", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")

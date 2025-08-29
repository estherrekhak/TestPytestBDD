import pytest
from selenium import webdriver
import allure
import os
from dotenv import load_dotenv

# Load .env automatically
load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="append",
        default=os.getenv("BROWSERS", "chrome").split(","),
        help="Browser(s) to run tests against: chrome, edge. Can be specified multiple times."
    )
    parser.addoption(
        "--tags",
        action="store",
        default=os.getenv("TAGS", None),
        help="Run only scenarios with the given tag (e.g. --tags=smoke)"
    )
    parser.addoption(
        "--featurefiles",
        action="append",
        default=[x.strip() for x in os.getenv("FEATUREFILES", "").split(",") if x.strip()] or None,
        help="Feature file(s) to run (e.g. --featurefiles=features/add_to_cart.feature). Can be specified multiple times."
    )
    def pytest_bdd_apply_tag(tag, function):
        # Get tag selection from CLI or .env
        import pytest
        selected_tags = pytest.config.getoption("tags")
        if selected_tags:
            # Support comma-separated tags
            selected = [t.strip() for t in selected_tags.split(",") if t.strip()]
            if tag not in selected:
                return True  # skip scenario if tag does not match
        return None  # run scenario

@pytest.fixture
def browser(request, browser_type):
    # Use browser_type from test parameter for correct parallel execution
    driver = None
    try:
        if browser_type == "chrome":
            print("Launching Chrome browser...")
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager
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
            # Remove headless mode for headed execution
            # chrome_options.add_argument("--headless")  # Commented out for headed mode
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        elif browser_type == "edge":
            print("Launching Edge browser...")
            from selenium.webdriver.edge.options import Options as EdgeOptions
            from selenium.webdriver.edge.service import Service as EdgeService
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            edge_options = EdgeOptions()
            edge_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "safebrowsing.enabled": False,
                "safebrowsing.disable_download_protection": True
            })
            edge_options.add_argument("--disable-notifications")
            edge_options.add_argument("--disable-background-networking")
            edge_options.add_argument("--headless")  # optional for CI
            edge_options.add_argument("--no-sandbox")
            # Use a unique user-data-dir for parallel tests
            import uuid
            unique_profile = f"/tmp/edge-profile-{uuid.uuid4()}"
            edge_options.add_argument(f"--user-data-dir={unique_profile}")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option("useAutomationExtension", False)
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
            print("Edge browser launched. Current URL:", driver.current_url)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
    except Exception as e:
        print(f"Error launching {browser_type} browser: {e}")
        raise
    try:
        yield driver
    finally:
        print(f"Quitting {browser_type} browser. Current URL: {driver.current_url if driver else 'N/A'}")
        if driver:
            driver.quit()

def pytest_generate_tests(metafunc):
    if "browser" in metafunc.fixturenames or "browser_type" in metafunc.fixturenames:
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

@pytest.fixture
def browser_type(request):
    # Get browser_type from test parameterization (set by pytest_generate_tests)
    return request.param if hasattr(request, 'param') else request.config.getoption("browser")[0]

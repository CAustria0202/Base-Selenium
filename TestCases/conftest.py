import os
import time
import pytest
import configparser
from selenium import webdriver
#Chrome Browser
from selenium.webdriver.chrome.service import Service as ServiceChrome
from webdriver_manager.chrome import ChromeDriverManager
#Chromium Browser
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType
#Firefox Browser
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
#Edge Browser
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def get_config():
    config = configparser.ConfigParser()

    # Get the path of the directory where conftest.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "..", "config.ini")  # Adjust to go one level up to find config.ini

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    config.read(config_path)

    #Added os.getenv for adding parametization option when using Jenkins
    browser = os.getenv('BROWSER', config.get("settings", "browser", fallback="chrome"))
    url = os.getenv('URL', config.get("settings", "url", fallback="https://google.com/"))
    head = os.getenv('HEADLESS', config.getboolean("settings", "head", fallback=False))

    print(f"Selected browser: {browser}")
    print(f"Selected URL: {url}")
    print(f"Headless: {head}")
    return browser, url, head

@pytest.fixture(autouse=True)
def setup(request):
        browser, url, head = get_config()
        if browser == "chrome":
            chrome_options = webdriver.ChromeOptions()
            if head:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(service=ServiceChrome(ChromeDriverManager().install()), options=chrome_options)
        elif browser == "chromium":
            chromium_options = webdriver.ChromeOptions()
            if head:
                chromium_options.add_argument('--headless')
                chromium_options.add_argument('--no-sandbox')
                chromium_options.add_argument('--disable-gpu')
                chromium_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chromium_options)
        elif browser == "firefox":
            firefox_options = webdriver.FirefoxOptions()
            if head:
                firefox_options.add_argument('--headless')
                firefox_options.add_argument('--no-sandbox')
                firefox_options.add_argument('--disable-gpu')
                firefox_options.add_argument('--window-size=1920,1080')
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
        elif browser == "edge":
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.get(url)
        driver.maximize_window()
        request.cls.driver = driver
        yield driver
        driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, directory="Screenshot" ,filename_prefix="screenshot"):
    outcome = yield
    report = outcome.get_result()

    # If test fails during the "call" phase, take a screenshot
    if report.when == "call" and report.failed:
        driver = getattr(item.cls, "driver", None)  # Get driver from test context
        if driver:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root directory
            screenshot_dir = os.path.join(base_dir, directory)

            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"failed_{filename_prefix}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"🔥 Screenshot taken on failure: {screenshot_path}")
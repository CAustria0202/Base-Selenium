import os
import time
from selenium.webdriver.support.wait import WebDriverWait
from Base.base_driver import BaseDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class Utils(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    #Verify the alert message matched the expected message
    def verify_alert(self, expected_message):
        alert = self.driver.switch_to.alert
        assert alert.text == expected_message, f"Alert message did not match! Expected: '{expected_message}', Found: '{alert.text}'"
        alert.accept()

    # Wait for the page to fully load by checking the document ready state
    def wait_for_page_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("Page fully loaded.")
        except Exception as e:
            print(f"Page did not load within {timeout} seconds: {e}")

    def assert_page_contains_text(self, expected_text, error_message=None):
        """
        Assert that a specific text is present in the page source.

        :param expected_text: The text expected to be found on the page
        :param error_message: Custom error message (optional)
        """
        error_message = error_message or f"{expected_text} was not found on the page"
        assert expected_text in self.driver.page_source, error_message

    @staticmethod
    def assert_element_to_have_text(expected_text, actual_text,  message="Element did not have text"):
        assert expected_text in actual_text, f"{message}\n Expected: '{expected_text}', Found: '{actual_text}'"

    # Assert if the actual text matches the expected text
    @staticmethod
    def assert_element_text(expected_text, actual_text, message="Text did not match!"):
        assert expected_text == actual_text, f"{message}\nExpected: '{expected_text}', Found: '{actual_text}'"

    @staticmethod
    def assert_element_exists(element, error_message=None):
        """
        Assert that a given web element is present on the page.

        :param element: Web element to check.
        :param error_message: Custom error message (optional).
        """
        error_message = error_message or f"{element} was not found on the page"
        assert element is not None, error_message
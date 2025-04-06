from selenium.webdriver.common.by import By
from Base.base_driver import BaseDriver
from Utilities.utils import Utils

class SamplePage(BaseDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.image_input_locator = (By.ID, "locator")

    def upload_profile_picture(self, file_path: str) -> bool:
        return Utils.upload_image_file(self.driver, self.image_input_locator, file_path)
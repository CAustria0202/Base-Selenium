import os
import pytest
from Base.base_driver import BaseDriver
from Utilities.utils import Utils
from Pages.sample_page import SamplePage


@pytest.mark.usefixtures("setup")
class TestBaseSample:

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.driver = setup
        self.base_drive = BaseDriver(self.driver)
        self.utils = Utils(self.driver)
        self.registration = SamplePage(self.driver)

    def test_upload_valid_image(self):

        image_path = os.path.abspath("test_data/sample_image.jpg")
        result = self.registration.upload_profile_picture(image_path)

        assert result is True, "Image upload should succeed with valid image file"

    def test_upload_invalid_file(self):

        non_image_path = os.path.abspath("test_data/sample_document.pdf")
        result = self.registration.upload_profile_picture(non_image_path)

        assert result is False, "Image upload should fail with non-image file"
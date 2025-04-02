import pytest
from Base.base_driver import BaseDriver
from Utilities.utils import Utils


@pytest.mark.usefixtures("setup")
class TestBaseSample:

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.driver = setup
        self.base_drive = BaseDriver(self.driver)
        self.utils = Utils(self.driver)

    # def test_sample_base(self):
    #
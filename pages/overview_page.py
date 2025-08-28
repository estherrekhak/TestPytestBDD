from selenium.webdriver.common.by import By
from .base_page import BasePage

class OverviewPage(BasePage):
    OVERVIEW_TITLE = (By.CLASS_NAME, 'title')

    def get_overview_title(self):
        return self.find_element(self.OVERVIEW_TITLE).text

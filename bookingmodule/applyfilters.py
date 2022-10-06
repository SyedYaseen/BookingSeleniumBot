from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class ApplyFilters:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def select_stars(self, *stars):
        star_filter_box = self.driver.find_element(
            By.CSS_SELECTOR, 'div[data-filters-group="class"]')

        for star_value in stars:
            star_filter_box.find_element(By.CSS_SELECTOR, f'div[data-filters-item="class:class={star_value}"]').click()

    def get_result(self):
        return self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')





import BookingComBot.bookingmodule.constants as const
import BookingComBot.bookingmodule.utils as utils
from BookingComBot.bookingmodule.applyfilters import ApplyFilters
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
import pandas as pd


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r";C:\SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += r';C:\SeleniumDrivers'
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_experimental_option('detach', True)

        super(Booking, self).__init__(options=options)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_landing_page(self):
        self.get(const.BASE_URL)

    def reject_cookies(self):
        decline_cookies = WebDriverWait(self, 30).until(
            EC.presence_of_element_located((By.ID, "onetrust-reject-all-handler"))
        )
        decline_cookies.click()

    def change_currency(self, currency="USD"):
        choose_currency = self.find_element(
            By.CSS_SELECTOR, 'button[data-modal-aria-label="Select your currency"]')
        choose_currency.click()

        select_currency = self.find_element(
            By.CSS_SELECTOR, f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        select_currency.click()

    def search(self, search_value='Amsterdam'):
        search_bar = self.find_element(By.ID, "ss")
        search_bar.send_keys(search_value)
        self.implicitly_wait(30)
        WebDriverWait(self, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[data-i="0"]'))).click()

        # first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        # first_result.click()

    def trip_dates(self, start_date, return_date):
        month_difference = utils.months_calc(start_date, return_date)
        calendar_next = self.find_element(By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]')

        for i in range(month_difference['start_months']):
            calendar_next.click()
        start_date_el = self.find_element(By.CSS_SELECTOR, f'td[data-date="{start_date}"]')
        start_date_el.click()

        for i in range(month_difference['return_months'] - month_difference['start_months']):
            calendar_next.click()
        return_date_el = self.find_element(By.CSS_SELECTOR, f'td[data-date="{return_date}"]')
        return_date_el.click()

    def no_people(self, num_of_adults):
        number_of_adults = int(num_of_adults)
        guests_toggle = self.find_element(By.ID, "xp__guests__toggle")
        guests_toggle.click()

        no_adults = self.find_element(By.ID, "group_adults")
        current_no_of_adults = int(no_adults.get_attribute("value"))

        increase_adults_btn = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
        decrease_adults_btn = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')

        if current_no_of_adults<number_of_adults:
            for _ in range(current_no_of_adults, number_of_adults):
                increase_adults_btn.click()

        if current_no_of_adults>number_of_adults:
            for _ in reversed(range(number_of_adults, current_no_of_adults)):
                decrease_adults_btn.click()


    def search_btn(self):
        search_btn = self.find_element(By.CLASS_NAME, "xp__button")
        search_btn.click()


    def apply_filters(self):
        filters = ApplyFilters(self)
        filters.select_stars(4,5)
        return filters.get_result()


    def get_report(self):
        # filteredResults = self.apply_filters()
        time.sleep(5)
        report = []
        df_report = pd.DataFrame(
            columns=['Title', 'Price', 'Link'])

        wait = WebDriverWait(self, 60)

        titleList = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-testid="title"]')
        ))
        linkList = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'a[data-testid="title-link"]')))
        priceList = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[data-testid="price-and-discounted-price"]')
        ))

        for i in range(0, len(linkList)):
            priceValue = priceList[i].find_element(By.CSS_SELECTOR, 'span:last-child').get_attribute('innerHTML')
            title = titleList[i].get_attribute('innerHTML')
            link = linkList[i].get_attribute('href')
            price = re.findall(r'\d+', priceValue)[0]

            # report.append([title,price,link])
            temp_df = pd.DataFrame([[title,price,link]], columns = ['Title', 'Price', 'Link'])
            df_report=pd.concat([df_report, temp_df])


        print(df_report)












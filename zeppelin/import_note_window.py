import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .main_page import MainPage


class ImportNoteWindow:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        logging.info('[Import Note Window] Waiting to load')
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="noteImportName"]')))
        time.sleep(1)  # TODO: Remove timeout

    def set_name(self, name):
        logging.info('[Import Note Window] set import name' + name)
        self.driver.browser.find_element_by_xpath('//input[@id="noteImportName"]').send_keys(name)

    def set_file(self, file):
        logging.info('[Import Note Window] set import file' + file)
        self.driver.browser.find_element_by_xpath('//*[@id="noteImportFile"]').send_keys(file)
        return MainPage(self.driver)

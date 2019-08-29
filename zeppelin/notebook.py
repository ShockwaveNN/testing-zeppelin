import codecs
import json
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Notebook:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        logging.info('[Notebook page] Waiting to load')
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@class, "ace_text-input")]')))

    def type_note(self, note):
        logging.info('[Notebook page] Typing note: '+ note)
        self.driver.browser.find_element_by_xpath('//textarea[contains(@class, "ace_text-input")]').send_keys(note)

    def name(self):
        logging.info('[Notebook page] Getting notebook name')
        return self.driver.browser.find_element_by_xpath('//p[contains(@class, "form-control-title")]/span').text

    def export_note(self):
        logging.info('[Notebook page] Exporting note')
        self.driver.browser.find_element_by_xpath('//button[contains(@ng-click, "exportNote")]').click()
        file_path = self.driver.download_dir + "/" + self.name() + ".json"
        return json.load(codecs.open(file_path, 'r', 'utf-8-sig'))

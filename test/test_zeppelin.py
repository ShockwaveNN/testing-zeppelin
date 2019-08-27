from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="main"]//a[@data-target="#noteCreateModal"]')))

    def open_new_note_window(self):
        self.driver.find_element_by_xpath('//div[@id="main"]//a[@data-target="#noteCreateModal"]').click()
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="noteCreateModal"]//input[@id="noteName"]')))
        time.sleep(1)  # Remove timeout

    def create_new_note(self, name, interpreter='spark'):
        self.open_new_note_window()
        self.driver.find_element_by_xpath('//div[@id="noteCreateModal"]//input[@id="noteName"]').send_keys(name)
        # TODO: ability to set interpreter
        self.driver.find_element_by_xpath('//*[@id="createNoteButton"]').click()
        return Notebook(self.driver)


class Notebook:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@class, "ace_text-input")]')))

    def type_note(self, note):
        self.driver.find_element_by_xpath('//textarea[contains(@class, "ace_text-input")]').send_keys(note)

    def export_note(self):
        self.driver.find_element_by_xpath('//button[contains(@ng-click, "exportNote")]').click()


def start_browser():
    chromedriver_path = r'/usr/bin/chromedriver'
    return webdriver.Chrome(executable_path=chromedriver_path)


def test_export():
    driver = start_browser()
    driver.get('http://localhost:8080')
    main_page = MainPage(driver)
    note_page = main_page.create_new_note('note_name')
    note_page.type_note('note_content')
    note_page.export_note()
    driver.quit()

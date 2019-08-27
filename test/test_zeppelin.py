from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import tempfile
import json
import codecs


class Browser:
    download_dir = tempfile.mkdtemp()
    chromedriver_path = r'/usr/bin/chromedriver'

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.download_dir}
        chrome_options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=chrome_options)

    def open(self, url):
        self.browser.get(url)

    def quit(self):
        self.browser.quit


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="main"]//a[@data-target="#noteCreateModal"]')))

    def open_new_note_window(self):
        self.driver.browser.find_element_by_xpath('//div[@id="main"]//a[@data-target="#noteCreateModal"]').click()
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="noteCreateModal"]//input[@id="noteName"]')))
        time.sleep(1)  # Remove timeout

    def create_new_note(self, name, interpreter='spark'):
        self.open_new_note_window()
        self.driver.browser.find_element_by_xpath('//div[@id="noteCreateModal"]//input[@id="noteName"]').send_keys(name)
        # TODO: ability to set interpreter
        self.driver.browser.find_element_by_xpath('//*[@id="createNoteButton"]').click()
        return Notebook(self.driver)


class Notebook:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@class, "ace_text-input")]')))

    def type_note(self, note):
        self.driver.browser.find_element_by_xpath('//textarea[contains(@class, "ace_text-input")]').send_keys(note)

    def name(self):
        return self.driver.browser.find_element_by_xpath('//p[contains(@class, "form-control-title")]/span').text

    def export_note(self):
        self.driver.browser.find_element_by_xpath('//button[contains(@ng-click, "exportNote")]').click()
        file_path =self.driver.download_dir + "/" + self.name() + ".json"
        return json.load(codecs.open(file_path, 'r', 'utf-8-sig'))


def test_export():
    driver = Browser()
    driver.open('http://localhost:8080')
    main_page = MainPage(driver)
    note_page = main_page.create_new_note('note_name')
    note_page.type_note('note_content')
    note_data = note_page.export_note()
    assert note_data['name'] == 'note_name'
    assert note_data['paragraphs'][0]['text'] == 'note_content'
    driver.quit()

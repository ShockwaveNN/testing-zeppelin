import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from faker import Faker
import time
import tempfile
import json
import codecs
import requests
import logging

class Browser:
    download_dir = tempfile.mkdtemp()
    chromedriver_path = r'/usr/bin/chromedriver'

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': self.download_dir}
        chrome_options.add_experimental_option('prefs', prefs)
        logging.info('Starting browser')
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=chrome_options)

    def open(self, url):
        logging.info('Opening url: ' + url)
        self.browser.get(url)

    def quit(self):
        logging.info('Closing browser')
        self.browser.quit()


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait_to_load()

    def wait_to_load(self):
        logging.info('[Main Page] Waiting to load')
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="main"]//a[@data-target="#noteCreateModal"]')))
        time.sleep(1)  # TODO: Remove timeout

    def open_new_note_window(self):
        logging.info('[Main Page]Open new note window')
        self.driver.browser.find_element_by_xpath('//div[@id="main"]//a[@data-target="#noteCreateModal"]').click()
        WebDriverWait(self.driver.browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="noteCreateModal"]//input[@id="noteName"]')))
        time.sleep(1)  # TODO: Remove timeout

    def create_new_note(self, name, interpreter='spark'):
        logging.info('[Main Page] Create new note with name: ' + name)
        self.open_new_note_window()
        self.driver.browser.find_element_by_xpath('//div[@id="noteCreateModal"]//input[@id="noteName"]').send_keys(name)
        # TODO: ability to set interpreter
        self.driver.browser.find_element_by_xpath('//*[@id="createNoteButton"]').click()
        return Notebook(self.driver)

    def import_note(self):
        logging.info('[Main Page] Click on import note')
        self.driver.browser.find_element_by_xpath('//div[@id="main"]//a[@data-target="#noteImportModal"]').click()
        return ImportNoteWindow(self.driver)

    def open_note_by_name(self, name):
        logging.info('[Main Page] Opening note with name: ' + name)
        #TODO: handle opening note by name
        return Notebook(self.driver)


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


class ZeppelinApi:
    def __init__(self, url):
        self.url = url

    def notes(self):
        import urllib.request
        logging.info('[ZeppelinApi] Get list of all notes')
        data = urllib.request.urlopen(self.url + "/api/notebook").read()
        return json.loads(data)['body']

    def delete_note_by_id(self, note_id):
        logging.info('[ZeppelinApi] delete_note_by_id: ' + note_id)
        requests.delete(self.url + "/api/notebook/" + note_id)

    def delete_note_by_name(self, name):
        logging.info('[ZeppelinApi] Delete note by name: ' + name)
        notes = self.notes()
        note = next(item for item in notes if item["name"] == name)
        self.delete_note_by_id(note['id'])


@pytest.fixture(autouse=True)
def note_name():
    yield Faker().job()


@pytest.fixture(autouse=True)
def note_content():
    yield Faker().text(50)

@pytest.fixture(autouse=True)
def note_file():
    yield '/home/lobashov/sources/testing-zeppelin/zeppelin/PermanentTestNote.json' # TODO relative path

@pytest.fixture(autouse=True)
def open_zeppelin(note_name):
    api = ZeppelinApi('http://localhost:8080')
    driver = Browser()
    driver.open('http://localhost:8080')
    yield driver
    driver.quit()
    api.delete_note_by_name(note_name)


def test_export(open_zeppelin, note_name, note_content):
    main_page = MainPage(open_zeppelin)
    note_page = main_page.create_new_note(note_name)
    note_page.type_note(note_content)
    note_data = note_page.export_note()
    assert note_data['name'] == note_name
    assert note_data['paragraphs'][0]['text'] == note_content


def test_import(open_zeppelin, note_name, note_file):
    main_page = MainPage(open_zeppelin)
    import_note_window = main_page.import_note()
    import_note_window.set_name(note_name)
    main_page = import_note_window.set_file(note_file)
    note_page = main_page.open_note_by_name(note_name)
    assert note_page.name == note_name

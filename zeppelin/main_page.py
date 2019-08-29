import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .notebook import Notebook


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
        logging.info(f"[Main Page] Create new note with name: {name}")
        self.open_new_note_window()
        self.driver.browser.find_element_by_xpath('//div[@id="noteCreateModal"]//input[@id="noteName"]').send_keys(name)
        # TODO: ability to set interpreter
        self.driver.browser.find_element_by_xpath('//*[@id="createNoteButton"]').click()
        return Notebook(self.driver)

    def import_note(self):
        logging.info('[Main Page] Click on import note')
        self.driver.browser.find_element_by_xpath('//div[@id="main"]//a[@data-target="#noteImportModal"]').click()
        return ImportNoteWindow(self.driver)

    def notes_names(self):
        notes_objects = self.driver.browser.find_elements_by_xpath("//ul[@id='notebook-names']/div//li//a[1]")
        names = [x.text for x in notes_objects]
        logging.info(f'[Main Page] Get list of all notes {names}')
        return names

    def open_note_by_name(self, name):
        logging.info(f"[Main Page] Opening note with name: {name}")
        note_index = self.notes_names().index(name)
        self.driver.browser.find_element_by_xpath(f"(//ul[@id='notebook-names']/div//li)[{note_index + 1}]//a[1]").click()
        # TODO: handle opening note by name
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
        logging.info(f"[Import Note Window] set import name {name}")
        self.driver.browser.find_element_by_xpath('//input[@id="noteImportName"]').send_keys(name)

    def set_file(self, file):
        logging.info(f"[Import Note Window] set import file {file}")
        self.driver.browser.find_element_by_xpath('//*[@id="noteImportFile"]').send_keys(file)
        return MainPage(self.driver)
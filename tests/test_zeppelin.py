import os
import pytest
from faker import Faker
from zeppelin.browser import Browser
from zeppelin.main_page import MainPage
from zeppelin.notebook import Notebook
from zeppelin.zeppelin_api import ZeppelinApi


@pytest.fixture(autouse=True)
def note_name():
    yield Faker().job()


@pytest.fixture(autouse=True)
def note_content():
    yield Faker().text(50)

@pytest.fixture(autouse=True)
def note_file():
    yield os.getcwd() + '/tests/PermanentTestNote.json'

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
    assert note_name not in main_page.notes_names()
    import_note_window = main_page.import_note()
    import_note_window.set_name(note_name)
    main_page = import_note_window.set_file(note_file)
    assert note_name in main_page.notes_names()
    note_page = main_page.open_note_by_name(note_name)
    assert note_page.name() == note_name

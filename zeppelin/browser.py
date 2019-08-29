import logging
import tempfile
from selenium import webdriver


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

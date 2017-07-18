import os
import base64
import logging, logging.config
from selenium.webdriver.common.by import By


CUR_DIR = os.path.dirname(__file__)

#######################
#       Config        #
#######################
logging.config.fileConfig(os.path.join(CUR_DIR, '..',"logger.conf"))

#######################
#     JS Scripts      #
#######################
def get_js(name):
    with open(os.path.join(CUR_DIR, '..', 'js', name), 'rb') as f:
        return f.read().decode('utf-8')


class Base:
    # Logger
    LOGGER = logging.getLogger("dev")

    # JS Scripts
    getDataURL_js = get_js('getDataURL.js')

    # collect menu episode urls
    episodes = []

    # Below attribute should be override
    # Match
    menu = None         # URL pattern
    page = None         # URL pattern

    # Menu page
    episode_name = ''   # locator
    episode = ''        # locator

    # View page
    image = ''          # locator
    next_page = ''      # locator


    def __init__(self, menu_url='', page_url='', browser=None):
        self.menu_url = menu_url
        self.page_url = page_url
        self.browser = browser


    #######################
    #       Setting       #
    #######################
    def set_browser(self, browser):
        self.browser = browser

    def _set_episodes(self):
        elements = self.browser.find_elements_by_css_selector(self.episode)
        for i in elements:
            self.episodes.append(i.get_attribute('href'))


    #######################
    #      Download       #
    #######################
    def download(self):
        pass

    def _download_episodes(self):
        for episode in self.episodes:
            self.browser.get(episode)
            self._download_episode()

    def _download_episode(self):
        self.download_page()    # first page
        while self._next_page():
            self._download_page()

    def _download_page(self):
        data = self._get_data_url()
        self._save_as_file(data, 'test.png')

    # for test
    def download_page(self, page_url):
        self.browser.get(page_url)
        data = self._get_data_url()
        self._save_as_file(data, 'test.png')


    #######################
    #       Action        #
    #######################
    def _next_page(self):
        next_page_button = self.find_elements_by_css_selector(self.next_page)
        if len(next_page_button) == 0:
            return False
        next_page_button = next_page_button[0]
        if next_page_button.is_displayed():
            next_page_button.click()
            return True


    #######################
    #     Save Image      #
    #######################
    def _get_data_url(self):
        data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % self.getDataURL_js, self.image)
        if not data_base64:
            self.LOGGER.error("Don't get data url")
        self.LOGGER.debug('Get data URL %s ...' % data_base64[:50])
        return data_base64[22:]

    def _save_as_file(self, data_base64, path):
        data = base64.b64decode(data_base64.encode('ascii'))
        with open(path, 'wb') as f:
            f.write(data)
        self.LOGGER.info('Save image as %s' % path)

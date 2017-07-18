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
    menu = None   # URL pattern
    page = None   # URL pattern

    # Menu page
    episode_name = ''   # locator
    episode = ''        # locator

    # View page
    image = ''          # locator
    next_page = ''      # locator
    next_episode = ''   # locator


    def __init__(self, menu_url='', page_url='', browser=None):
        self.menu_url = menu_url
        self.page_url = page_url
        self.browser = browser

    def set_browser(self, browser):
        self.browser = browser

    def get_episodes(self):
        pass

    def download(self, page_url):
        pass

    def download_page(self, page_url):
        self.browser.get(page_url)
        data = self.get_data_url()
        self.save_as_file(data, 'test.png')

    def get_data_url(self):
        data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % self.getDataURL_js, self.image)
        if not data_base64:
            self.LOGGER.error("Don't get data url")
        self.LOGGER.debug('Get data URL %s ...' % data_base64[:50])
        return data_base64[22:]

    def save_as_file(self, data_base64, path):
        data = base64.b64decode(data_base64.encode('ascii'))
        with open(path, 'wb') as f:
            f.write(data)
        self.LOGGER.info('Save image as %s' % path)

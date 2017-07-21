import os
import base64
import logging, logging.config


CUR_DIR = os.path.dirname(__file__)

#######################
#       Config        #
#######################
logging.config.fileConfig(os.path.join(CUR_DIR, '..',"logger.conf"))

#######################
#       Scripts       #
#######################
def get_js(name):
    with open(os.path.join(CUR_DIR, '..', 'js', name), 'rb') as f:
        return f.read().decode('utf-8')

class Script:

    getDataURL_js = get_js('getDataURL.js')
    getDataURL_js2 = get_js('getDataURL2.js')
    redirect_js = get_js('redirect.js')


class Base:
    # Logger
    LOGGER = logging.getLogger("dev")

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
            self.episodes.append((i.get_attribute('text'),i.get_attribute('href')))


    #######################
    #      Download       #
    #######################
    def download(self):
        if self.page_url:
            self.browser.get(self.page_url)
            self._download_episode()
        elif self.menu_url:
            self.browser.get(self.menu_url)
            self._set_episodes()
            self._download_episodes()
        else:
            self.LOGGER.error("URL is empty")

    def _download_episodes(self):
        for episode in self.episodes:
            for title, href in episode:
                self.redirect(href)
                self._download_episode()

    def _download_episode(self):
        self._download_page()    # first page
        while self._next_page():
            self._download_page()

    def _download_page(self):
        name = self._get_image_name()
        data = self._get_data_url()
        self._save_as_file(data, name)

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
    def _get_image_name(self):
        image = self.browser.find_elements_by_css_selector(self.image)
        if len(image) == 0:
            self.LOGGER.error("Don't find image by selector: %s" % self.image)
            return False
        image = image[0]
        name = image.get_attribute('src').split('/')[-1]
        return name

    def _get_data_url(self):
        data_base64 = ''
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getDataURL_js, self.image)
            self.LOGGER.debug('Get data URL %s ...' % data_base64[:10])
        except:
            self.LOGGER.error("Don't get data url by getDataURL_js")
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getDataURL_js2, self.image)
            self.LOGGER.debug('Get data URL %s ...' % data_base64[:10])
        except:
            self.LOGGER.error("Don't get data url by getDataURL_js2")
        return data_base64

    def _save_as_file(self, data_base64, path):
        data = base64.b64decode(data_base64.encode('ascii'))
        with open(path, 'wb') as f:
            f.write(data)
        self.LOGGER.info('Save image as %s' % path)


    #######################
    #      Redirect       #
    #######################
    def redirect(self, url):
        self.browser.execute_script('(%s)(arguments[0]' % Script.redirect_js, url)

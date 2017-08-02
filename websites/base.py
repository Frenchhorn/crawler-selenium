import os
import base64


#######################
#       Scripts       #
#######################
def get_js(name):
    with open(os.path.join(os.path.dirname(__file__), '..', 'js', name), 'rb') as file:
        return file.read().decode('utf-8')

class Script:

    getImage_js = get_js('getImage.js')
    getDataURL_js = get_js('getDataURL.js')
    redirect_js = get_js('redirect.js')


class Base:

    # collect menu episode urls
    episodes = []

    # Below attribute should be overrided
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

    def set_logger(self, logger):
        self.LOGGER = logger

    def _set_episodes(self):
        elements = self.browser.find_elements_by_css_selector(self.episode)
        for i in elements:
            self.episodes.append((i.get_attribute('text'), i.get_attribute('href')))


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
    def test(self):
        page_url = self.page_url
        self.LOGGER.info('Enter page %s' % page_url)
        self.browser.get(page_url)
        self.LOGGER.info('Get data')
        data = self._get_data_url()
        self.LOGGER.info('Save data')
        self._save_as_file(data, 'test.png')
        self.browser.quit()


    #######################
    #       Action        #
    #######################
    def _next_page(self):
        next_page_button = self.browser.find_elements_by_css_selector(self.next_page)
        if not next_page_button:
            return False
        next_page_button = next_page_button[0]
        if next_page_button.is_displayed():
            next_page_button.click()
            return True


    #######################
    #     Save Image      #
    #######################
    def save_image(self):
        data_base64 = ''
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getImage_js, self.image)
            self.LOGGER.debug('Get data URL %s ...' % data_base64[:10])
        except:
            pass
        if not data_base64:
            return False
        data = base64.b64decode(data_base64.encode('ascii'))
        with open('test.png', 'wb') as file:
            file.write(data)
        self.LOGGER.info('Save image as test.png')
        return True

    def _get_image_name(self):
        image = self.browser.find_elements_by_css_selector(self.image)
        if not image:
            self.LOGGER.error("Don't find image by selector: %s" % self.image)
            return False
        image = image[0]
        name = image.get_attribute('src').split('/')[-1]
        return name

    def _get_data_url(self):
        data_base64 = ''
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getImage_js, self.image)
            self.LOGGER.debug('getDataURL_js: Get data URL %s ...' % data_base64[:10])
        except:
            self.LOGGER.error("Don't get data url by getDataURL_js")
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getDataURL_js, self.image)
            self.LOGGER.debug('getImage_js: Get data URL %s ...' % data_base64[:10])
        except:
            self.LOGGER.error("Don't get data url by getImage_js")
        return data_base64

    def _save_as_file(self, data_base64, path):
        data = base64.b64decode(data_base64.encode('ascii'))
        with open(path, 'wb') as file:
            file.write(data)
        self.LOGGER.info('Save image as %s' % path)


    #######################
    #      Redirect       #
    #######################
    def redirect(self, url):
        self.browser.execute_script('(%s)(arguments[0])' % Script.redirect_js, url)

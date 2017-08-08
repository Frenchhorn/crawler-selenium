"""
    Basic class for other website class in same folder
"""

import os
import base64


#######################
#       Scripts       #
#######################
def get_js(name):
    """Convert the js file to str.
    """
    with open(os.path.join(os.path.dirname(__file__), '..', 'js', name), 'rb') as file:
        return file.read().decode('utf-8')

class Script:
    """Keep the js file string.
    """
    getImage_js = get_js('getImage.js')
    getDataURL_js = get_js('getDataURL.js')
    redirect_js = get_js('redirect.js')


class Base:
    """Basic class for other website class in same folder.
    """

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
        """Set the browser of this instance.
        """
        self.browser = browser

    def set_logger(self, logger):
        """Set the logger from outer.
        """
        self.LOGGER = logger


    #######################
    #      Download       #
    #######################
    def download(self):
        """Start Download.
        """
        if self.page_url:
            self.browser.get(self.page_url)
            self.download_episode()
        elif self.menu_url:
            self.browser.get(self.menu_url)
            self.download_episodes()
        else:
            self.LOGGER.error("URL is empty")

    def download_episodes(self):
        """Start download in menu page.
        """
        episodes = self.browser.find_elements_by_css_selector(self.episode)
        for episode in episodes:
            episode.click()
            self.download_episode()
            self.browser.back()

    def download_episode(self):
        """Start download in view page
        """
        self.save_image()
        while self._next_page():
            self.save_image()


    #######################
    #        Test         #
    #######################
    def test(self):
        """Test save_image function.
        """
        self.LOGGER.info('Enter page %s' % self.page_url)
        self.browser.get(self.page_url)
        self.save_image()
        self.browser.quit()


    #######################
    #       Action        #
    #######################
    def _next_page(self):
        """Click next page button.
        """
        next_page_button = self.browser.find_elements_by_css_selector(self.next_page)
        if not next_page_button:
            return False
        next_page_button = next_page_button[0]
        if next_page_button.is_displayed():
            next_page_button.click()
            return True
        return False


    #######################
    #     Save Image      #
    #######################
    def save_image(self):
        """Save picture.
        """
        data_base64 = ''
        try:
            data_base64 = self.browser.execute_script('return (%s)(arguments[0])' % Script.getImage_js, self.image)
            self.LOGGER.debug('Get data URL %s ...' % data_base64[:10])
        except:
            pass
        if not data_base64:
            self.LOGGER.error('Can not get data.')
            return False
        data = base64.b64decode(data_base64.encode('ascii'))
        with open('test.png', 'wb') as file:
            file.write(data)
        self.LOGGER.info('Save image as test.png')
        return True


    #######################
    #      Redirect       #
    #######################
    def redirect(self, url):
        """Redirect the website
        """
        self.browser.execute_script('(%s)(arguments[0])' % Script.redirect_js, url)

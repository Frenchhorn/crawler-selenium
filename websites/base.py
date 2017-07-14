from selenium.webdriver.common.by import By


#######################
#     JS Scripts      #
#######################
def get_js(name):
    with open(os.path.join('..', 'js', name), 'rb') as f:
        return f.read().decode('utf-8')


class Base:
    # JS Scripts
    getDataURL_js = get_js('getDataURL.js')

    # Menu page
    episode = ''
    episodes = []
    episode_name = ''

    # View page
    image = ''
    next_page = ''
    next_episode = ''

    def __init__(self, menu_url='', page_url='', browser=None):
        self.menu_url = menu_url
        self.page_url = page_url
        self.browser = browser

    def set_browser(self, browser):
        self.browser = browser

    def get_episodes(self):
        pass

    def download(self, page_url):
        self.browser.get(page_url)

#######################
#       Logger        #
#######################
import logging, logging.config
logging.config.fileConfig("logger.conf")
LOGGER = logging.getLogger("dev")


#######################
#       Browser       #
#######################
import os
from selenium import webdriver

PHANTOMJS_PATH = os.path.join('.', 'driver', 'phantomjs.exe')
CHROME_PATH = os.path.join('.', 'driver', 'chromedriver.exe')
FIREFOX_PATH = os.path.join('.', 'driver', 'geckodriver.exe')
IE_PATH = os.path.join('.', 'driver', 'IEDriverServer.exe')
# phantomjs, chrome, firefox, ie
BROWSER = 'phantomjs'

def get_browser(browser=BROWSER):
    """Get the webdriver.

    :param browser: (optional) Browser name
    :return: Instance of relevant webdriver.
    """

    if browser == 'phantomjs':
        LOGGER.info('Get browser Phantomjs')
        return webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, service_args=['--web-security=false'])
    elif browser == 'chrome':
        LOGGER.info('Get browser Chrome')
        return webdriver.Chrome(executable_path=CHROME_PATH)
    elif browser == 'firefox':
        LOGGER.info('Get browser Firefox')
        return webdriver.Firefox(executable_path=FIREFOX_PATH)
    elif browser == 'ie':
        LOGGER.info('Get browser IE')
        return webdriver.Ie(executable_path=IE_PATH)
    else:
        LOGGER.error('Invalid or unsupported browser name')


#######################
#     Filter URL      #
#######################
import websites
WEBSITES_CLASS = [websites.__dict__[i] for i in websites.__all__]

def get_website_object(url):
    """Get suitable website instance.

    :param url: the full path of website, should be the menu page or view page.
    :return: Instance of class in module websites.
    """

    for Website in WEBSITES_CLASS:
        if Website.menu.match(url):
            return Website(menu_url=url)
        elif Website.page.match(url):
            return Website(page_url=url)

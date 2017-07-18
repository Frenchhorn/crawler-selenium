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
    if browser == 'phantomjs':
        return webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
    elif browser == 'chrome':
        return webdriver.Chrome(executable_path=CHROME_PATH)
    elif browser == 'firefox':
        return webdriver.Firefox(executable_path=FIREFOX_PATH)
    elif browser == 'ie':
        return webdriver.Ie(executable_path=IE_PATH)
    else:
        LOGGER.error('Invalid or unsupported browser name')


#######################
#     Filter URL      #
#######################
import websites
websites_class = [websites.__dict__[i] for i in websites.__all__]

def get_website_object(url):
    for i in websites_class:
        if i.menu.match(url):
            return i(menu_url=url)
        elif i.page.match(url):
            return i(page_url=url)
    return None

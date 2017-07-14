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
#       Logger        #
#######################
import logging
import logging.config

logging.config.fileConfig(os.path.join('.',"logger.conf"))
LOGGER = logging.getLogger("dev")


#######################
#     JS Scripts      #
#######################
def get_js(name):
    with open(os.path.join('.', 'js', name), 'rb') as f:
        return f.read().decode('utf-8')

class Script:
    getDataURL_js = get_js('getDataURL.js')


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


#######################
#   Get Image Data    #
#######################
def get_data_url(browser, selector):
    data_base64 = browser.execute_script('return (%s)(arguments[0])' % Script.getDataURL_js, selector)
    if not data_base64:
        LOGGER.error("Don't get data url")
    LOGGER.debug('Get data URL %s ...' % data_base64[:50])
    return data_base64[22:]


#######################
#     Save Image      #
#######################
import base64

def save_as_file(data_base64, path):
    data = base64.b64decode(data_base64.encode('ascii'))
    with open(path, 'wb') as f:
        f.write(data)
    LOGGER.info('Save image as %s' % path)


#######################
#        Test         #
#######################
def test():
    t = get_browser('phantomjs')
    t.get('https://static.runoob.com/images/icon/html5.png')
    data = get_data_url(t, 'img')
    save_as_file(data, 'test.png')
    t.close()


if __name__ == '__main__':
    test()

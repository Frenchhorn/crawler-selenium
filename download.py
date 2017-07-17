import utils
from websites import *


def download(url):
    website_object = utils.get_website_object(url)
    assert website_object, "Don't match"
    browser = utils.get_browser()
    website_object.set_browser(browser)
    if website_object.menu_url:
        pass
    elif website_object.page_url:
        pass


if __name__ == '__main__':
    website_object = utils.get_website_object('https://static.runoob.com/images/icon/html5.png')
    browser = utils.get_browser()
    website_object.set_browser(browser)
    website_object.browser.get(website_object.page_url)
    data = utils.get_data_url(website_object.browser, website_object.image)
    utils.save_as_file(data, 'test.png')

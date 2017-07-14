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

import utils


SAVE_FOLDER = 'download'

def download(url):
    website_object = utils.get_website_object(url)
    assert website_object, "Don't match"
    browser = utils.get_browser()
    website_object.set_browser(browser)
    website_object.download()


if __name__ == '__main__':
    website_object = utils.get_website_object('http://phantomjs.org/')
    browser = utils.get_browser()
    website_object.set_browser(browser)
    website_object.download_page('http://phantomjs.org/')
    browser.quit()

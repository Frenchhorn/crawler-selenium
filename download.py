import utils


SAVE_FOLDER = 'download'

def download(url, folder=SAVE_FOLDER):
    """Download the pictures to appointed folder.

    :param url:
    :param folder: (optional)
    """

    website_object = utils.get_website_object(url)
    assert website_object, "Don't match"
    browser = utils.get_browser()
    website_object.set_browser(browser)
    website_object.download()


if __name__ == '__main__':
    utils.LOGGER.info('Get website object')
    website_object = utils.get_website_object('http://phantomjs.org/')
    browser = utils.get_browser()
    utils.LOGGER.info('Set browser')
    website_object.set_browser(browser)
    utils.LOGGER.info('Download page')
    website_object.download_page('http://phantomjs.org/')
    utils.LOGGER.info('Finish')
    browser.quit()
    utils.LOGGER.info('Quit')

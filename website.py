import os
import logging, logging.config
import websites
from selenium.webdriver import PhantomJS, Chrome, Firefox, Ie


class Website:
    """Manage the class in websites and the whole flow.
    """

    CUR_DIR = os.path.dirname(__file__)
    BROWSER = 'phantomjs'
    BROWSER_DRIVER = {
        'phantomjs' : (PhantomJS ,os.path.join(CUR_DIR, 'driver', 'phantomjs.exe')),
        'chrome' : (Chrome ,os.path.join(CUR_DIR, 'driver', 'chromedriver.exe')),
        'firefox' : (Firefox ,os.path.join(CUR_DIR, 'driver', 'geckodriver.exe')),
        'ie' : (Ie ,os.path.join(CUR_DIR, 'driver', 'IEDriverServer.exe'))
    }
    WEBSITES_CLASS = [websites.__dict__[i] for i in websites.__all__]
    logging.config.fileConfig("logger.conf")
    LOGGER = logging.getLogger("dev")


    def __init__(self, url, browser_name=None, save_folder=None):
        """Create the Object from websites according to the url and set the Object.

        :param url: The full path of website, should be the menu page or view page.
        :param browser_name: (optional) Browser name.
        :param save_folder: (optional) Save the image to the appointed folder.
        """

        self.object = None
        for Class in self.WEBSITES_CLASS:
            if Class.menu.match(url):
                self.object = Class(menu_url=url)
                self.LOGGER.info('Using class %s' % Class.__name__)
                break
            elif Class.page.match(url):
                self.object =  Class(page_url=url)
                self.LOGGER.info('Using class %s' % Class.__name__)
                break
        else:
            self.LOGGER.error('Unsupported website url')

        if self.object:
            browser_name = browser_name.lower() if browser_name else self.BROWSER
            browser_driver = self.BROWSER_DRIVER.get(browser_name)
            if not browser_driver:
                self.LOGGER.error('Invalid or unsupported browser name')
            Driver, driver_path = browser_driver
            if browser_name == 'phantomjs':
                browser = Driver(executable_path=driver_path, service_args=['--web-security=false'])
            else:
                browser = Driver(executable_path=driver_path)
            self.LOGGER.info('Get browser %s' % browser_name)
            self.object.set_browser(browser)
            self.object.set_logger(self.LOGGER)


    def download(self):
        """Start download.
        """

        self.object.download()

""" Bot written using reactivex """
from interactive_bots.commons.utils import init_chrome_driver

SITE_PATH = "http://www.diagnos-online.ru/symp.html"

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args)
    driver.get(SITE_PATH)

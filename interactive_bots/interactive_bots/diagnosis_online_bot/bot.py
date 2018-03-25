""" Functions for bot """
from interactive_bots.commons.utils import init_chrome_driver

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args.headless)
    return

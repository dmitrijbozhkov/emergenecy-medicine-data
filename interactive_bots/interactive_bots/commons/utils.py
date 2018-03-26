""" Common utilities """
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from csv import DictWriter

def parse_args(parser):
    """ Takes ArgumentParser and parses arguments """
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help="Path to output files",
        action="store",
        type=str)
    parser.add_argument(
        "-head",
        "--headless",
        required=False,
        help="Should browser be run headlessly",
        action="count")
    parser.add_argument(
        "-b",
        "--bot",
        required=True,
        help="Which bot should be used",
        action="store",
        type=str)
    return parser.parse_args()

def init_chrome_driver(is_headless):
    """ Initializes chrome driver"""
    if is_headless:
        options = Options()
        options.add_argument("--headless")
        return Chrome(chrome_options=options)
    else:
        return Chrome()

def open_output_file(path, columns):
    """ Opens or creates output file for writing """
    file = open(path, "w+")
    return {
        "file": file,
        "writer": DictWriter(file, columns)
    }

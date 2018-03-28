""" Common utilities """
from csv import DictWriter
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from itertools import combinations

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

class ExhaustOptions():
    """ Class that takes list length and goes through all possible variants of its items """
    def __init__(self, list_len):
        self.list_len = list_len
        self.positions = [x for x in range(0, list_len)]
        self.comb = []
        self.items = 1

    def _next_item(self, item_list):
        """ Returns next item combination from list """
        combine = self.comb.pop()
        return [item_list[i] for i in combine]

    def next(self, item_list):
        """ Returns variant of items """
        if self.comb:
            return self._next_item(item_list)
        elif self.items > self.list_len:
            raise StopIteration
        else:
            self.comb = list(combinations(self.positions, self.items))
            self.items += 1
            return self._next_item(item_list)

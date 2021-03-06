""" Common utilities """
from csv import DictWriter
from itertools import combinations
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def parse_args(parser):
    """ Takes ArgumentParser and parses arguments """
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        help="Path to database",
        action="store",
        type=str)
    parser.add_argument(
        "-s",
        "--scema",
        required=True,
        help="Path to database scema script",
        action="store",
        type=str)
    parser.add_argument(
        "-b",
        "--bot",
        required=True,
        help="Which bot should be used",
        action="store",
        type=str)
    parser.add_argument(
        "-head",
        "--headless",
        required=False,
        help="Should browser be run headlessly",
        action="count")
    parser.add_argument(
        "-bl",
        "--block",
        required=False,
        help="Path to ad blocking extension",
        action="store",
        type=str)
    return parser.parse_args()

def init_chrome_driver(args):
    """ Initializes chrome driver"""
    options = Options()
    if args.headless:
        options.add_argument("--headless")
    if args.block:
        options.add_argument("--load-extension=" + args.block)
    return Chrome(chrome_options=options)

def next_item_combination(items, acc, add_symptom):
    """ Selects next item combination """
    options = acc.next(items)
    for option in options:
        option.click()
        add_symptom.click()
    return options

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

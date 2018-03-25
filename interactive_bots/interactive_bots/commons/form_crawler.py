""" Classes for crawling on forms """
from functools import partial

class FormActionOptions():
    """ Action that needs to be done on form """
    def __init__(self, driver):
        self.counter = 0
        self.driver = driver
        self.navigate = None
        self.data = None
        self.action = None

    def set_actions(self, navigate, data, action=None):
        """ Sets form item action action """
        self.navigate = partial(navigate, self.driver)
        self.data = partial(data, self.driver)
        if action is None:
            self.action = lambda l, i: l[i]
        else:
            self.action = partial(action, self.driver)

    def reset_counter(self):
        """ Resets counter of action options """
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        items = self.navigate()
        if self.counter >= len(items):
            raise StopIteration()
        else:
            item = self.action(items, self.counter)
            self.counter += 1
            return self.data(item)

class FormCrawler():
    """ Goes through FormActionOption's and writes results to a file """
    def __init__(self, driver):
        self.driver = driver
        self.actions = []

    def add_action(self, action):
        """ Adds next action to make """
        self.actions.append(action)

    def remove_action(self, index):
        """ Removes action by index """
        del self.actions[index]

    def crawl(self, writer):
        """ Goes through actions and passes their output to writer """
        if not self.actions:
            raise IndexError("List of actions is empty")
        last_act = len(self.actions) - 1
        row = {}
        pointer = 0
        writer.writeheader()
        while pointer >= 0:
            try:
                row = {**row, **next(self.actions[pointer])}
            except StopIteration:
                pointer -= 1
            else:
                if pointer == last_act:
                    writer.writerow(row)
                else:
                    pointer += 1

""" Classes for crawling on forms """
from functools import partial

class FormActionOptions():
    """ Action that needs to be done on form """
    def __init__(self, driver):
        self.acc = 0
        self.driver = driver
        self.navigate = None
        self.data = None
        self.action = None

    def set_actions(self, navigate, action, data):
        """ Sets form item navigate, action and data """
        self.navigate = partial(navigate, self.driver)
        self.data = partial(data, self.driver)
        self.action = partial(action, self.driver)

    def reset_accumulator(self):
        """ Resets accumulator of action """
        self.acc = 0

    def __iter__(self):
        return self

    def __next__(self):
        items = self.navigate()
        self.acc = self.action(items, self.acc)
        if not self.acc:
            raise StopIteration()
        else:
            return self.data(self.acc)

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
                record = next(self.actions[pointer])
                if pointer == last_act:
                    for rows in record:
                        row.update(rows)
                        print(row)
                        writer.writerow(row)
                else:
                    row.update(record)
                    pointer += 1
            except StopIteration:
                self.actions[pointer].reset_accumulator()
                pointer -= 1

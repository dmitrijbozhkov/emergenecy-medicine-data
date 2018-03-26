""" Tests for form crawlers """
from unittest import TestCase, main
from unittest.mock import Mock
from functools import partial
from interactive_bots.commons.form_crawler import FormActionOptions, FormCrawler

class FormActionOptionsTestCase(TestCase):
    """ Test case for FormActionOptions class """
    def setUp(self):
        self.driver_mock = Mock()
        self.form_action = FormActionOptions(self.driver_mock)
        self.navigate_mock = Mock()
        self.action_mock = Mock()
        self.data_mock = Mock()

    def test_set_actions_should_set_navigate(self):
        """ set_actions should take function for navigate and make partial with driver """
        self.navigate_mock.side_effect = lambda x: self.assertTrue(self.driver_mock is x)
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.data_mock)
        self.form_action.navigate()

    def test_set_actions_should_set_data(self):
        """ set_actions should take function for data and make partial with driver """
        self.data_mock.side_effect = lambda x: self.assertTrue(self.driver_mock is x)
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.data_mock)
        self.form_action.data()

    def test_set_actions_should_set_action(self):
        """ set_actions should take function for action and make partial with driver """
        self.action_mock = lambda x: self.assertTrue(self.driver_mock is x)
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.action_mock)
        self.form_action.action()

    def test_reset_accumulator_should_set_acc_to_0(self):
        """ reset_accumulator should set acc to 0 """
        self.form_action.acc = 12
        self.form_action.reset_accumulator()
        self.assertEqual(self.form_action.acc, 0)

    def test_iteration_should_stop_iteration_if_acc_is_False(self):
        """ Iteration through actions should stop if accumulator passed from action is false """
        self.navigate_mock.return_value = []
        self.action_mock.return_value = False
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.data_mock)
        self.assertRaises(StopIteration, partial(next, self.form_action))

    def test_iteration_should_pass_acc_to_data(self):
        """ acc should be passed to data if True """
        acc = ["stuff"]
        self.navigate_mock.return_value = [1]
        self.action_mock.return_value = acc
        self.data_mock.side_effect = lambda d, a: self.assertTrue(a is acc)
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.data_mock)
        next(self.form_action)

    def test_iteration_should_return_from_data(self):
        """ Iteration through FormActionOptions should return wahtever data returned """
        val = 1
        self.navigate_mock.return_value = [1]
        self.data_mock.return_value = val
        self.form_action.set_actions(self.navigate_mock, self.action_mock, self.data_mock)
        self.assertEqual(next(self.form_action), val)

class FormCrawlerTestCase(TestCase):
    """ Test case for FormCrawler """
    def setUp(self):
        self.driver_mock = Mock()
        self.form_crawler = FormCrawler(self.driver_mock)

    def test_add_action_should_add_action_to_list(self):
        """ add_action method should append action to actions list """
        act = Mock()
        self.form_crawler.add_action(act)
        self.assertTrue(act is self.form_crawler.actions[0])

    def test_remove_action_should_remove_action(self):
        """ remove_action should remove action from actions list by given index """
        act = Mock()
        self.form_crawler.add_action(act)
        self.form_crawler.remove_action(0)
        self.assertEqual(len(self.form_crawler.actions), 0)

    def test_crawl_should_set_header(self):
        """ crawl should call writeheader before writing anything else """
        writer = Mock()
        option = FormActionOptions(Mock())
        option.set_actions(Mock(return_value=[]), Mock(return_value=False), Mock())
        self.form_crawler.add_action(option)
        self.form_crawler.crawl(writer)
        writer.writeheader.assert_called_once()

    def test_crawl_should_write_row_of_all_values(self):
        """ crawl should write row from dictionary with all the fields passed by actions data function """
        write_dict = {"foo": 1, "bar": 2}
        writer = Mock()
        writer.writerow = lambda d: self.assertEqual(d, write_dict)
        def counter(d, l, a):
            if not a:
                return True
            else:
                return False
        option1 = FormActionOptions(Mock())
        option2 = FormActionOptions(Mock())
        option1.set_actions(Mock(return_value=[1]), Mock(side_effect=counter), Mock(return_value={"foo": write_dict["foo"]}))
        option2.set_actions(Mock(return_value=[1]), Mock(side_effect=counter), Mock(return_value=[{"bar": write_dict["bar"]}]))
        self.form_crawler.add_action(option1)
        self.form_crawler.add_action(option2)
        self.form_crawler.crawl(writer)

    def test_crawl_should_throw_exception_if_actions_list_is_empty(self):
        """ crawl should throw IndexError if actions is empty """
        self.assertRaises(IndexError, partial(self.form_crawler.crawl, Mock()))

if __name__ == "__main__":
    main()

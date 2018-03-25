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

    def test_set_actions_should_set_navigate(self):
        """ set_actions should take function for navigate and make partial with driver """
        navigate = Mock(callable=lambda x: self.assertTrue(self.driver_mock is x))
        data = Mock()
        self.form_action.set_actions(navigate, data)
        self.form_action.navigate()

    def test_set_actions_should_set_data(self):
        """ set_actions should take function for data and make partial with driver """
        navigate = Mock()
        data = Mock(callable=lambda x: self.assertTrue(self.driver_mock is x))
        self.form_action.set_actions(navigate, data)
        self.form_action.data()

    def test_set_actions_should_set_action(self):
        """ set_actions should take function for action and make partial with driver """
        navigate = Mock()
        data = Mock()
        action = Mock(callable=lambda x: self.assertTrue(self.driver_mock is x))
        self.form_action.set_actions(navigate, data, action)
        self.form_action.action()

    def test_set_actions_should_set_action_if_None(self):
        """ set_actions should set action to lambda that returns element by given index if passed action function is None """
        navigate = Mock()
        data = Mock()
        self.form_action.set_actions(navigate, data)
        item = self.form_action.action([1, 2, 3], 0)
        self.assertEqual(item, 1)

    def test_iteration_should_stop_iteration(self):
        """ Iteration through FormActionOptions should stop if amount of list items returned from navigate is less or equal than counter """
        navigate = Mock(return_value=[])
        data = Mock()
        action = Mock()
        self.form_action.set_actions(navigate, data, action)
        self.assertRaises(StopIteration, partial(next, self.form_action))

    def test_iteration_should_increment_counter(self):
        """ Iteration through FormActionOptions should increment counter after each item """
        navigate = Mock(return_value=[1])
        data = Mock()
        action = Mock()
        self.form_action.set_actions(navigate, data, action)
        next(self.form_action)
        self.assertEqual(self.form_action.counter, 1)

    def test_iteration_should_return_from_data(self):
        """ Iteration through FormActionOptions should return wahtewer data returned """
        val = 1
        navigate = Mock(return_value=[1])
        data = Mock(return_value=val)
        action = Mock()
        self.form_action.set_actions(navigate, data, action)
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
        option.set_actions(Mock(return_value=[]), Mock())
        self.form_crawler.add_action(option)
        self.form_crawler.crawl(writer)
        writer.writeheader.assert_called_once()

    def test_crawl_should_write_row_of_all_values(self):
        """ crawl should write row from dictionary with all the fields passed by actions data function """
        write_dict = {"foo": 1, "bar": 2}
        writer = Mock()
        writer.writerow = lambda d: self.assertEqual(d, write_dict)
        option1 = FormActionOptions(Mock())
        option2 = FormActionOptions(Mock())
        option1.set_actions(Mock(return_value=[1]), Mock(return_value={"foo": write_dict["foo"]}))
        option2.set_actions(Mock(return_value=[1]), Mock(return_value={"bar": write_dict["bar"]}))
        self.form_crawler.add_action(option1)
        self.form_crawler.add_action(option2)
        self.form_crawler.crawl(writer)

    def test_crawl_should_throw_exception_if_actions_list_is_empty(self):
        """ crawl should throw IndexError if actions is empty """
        self.assertRaises(IndexError, partial(self.form_crawler.crawl, Mock()))

if __name__ == "__main__":
    main()

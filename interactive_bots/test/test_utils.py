""" Tests that always pass """
from unittest import TestCase, main
from unittest.mock import Mock
from interactive_bots.commons.utils import parse_args, init_chrome_driver

class ParseArgsTestCase(TestCase):
    """ Test case for parse_args function """
    def setUp(self):
        argparse_mock = Mock()
        self.argparse_mock = argparse_mock

    def test_set_path_command(self):
        """ --path command should be set """
        parse_args(self.argparse_mock)
        self.argparse_mock.add_argument.assert_any_call(
            "-p",
            "--path",
            required=True,
            help="Path to output files",
            action="store",
            type=str)

    def test_set_headless_command(self):
        """ --headless command should be set """
        parse_args(self.argparse_mock)
        self.argparse_mock.add_argument.assert_any_call(
            "-head",
            "--headless",
            required=False,
            help="Should browser be run headlessly",
            action="count")

    def test_set_bot_command(self):
        """ --bot command should be set """
        parse_args(self.argparse_mock)
        self.argparse_mock.add_argument.assert_any_call(
            "-b",
            "--bot",
            required=True,
            help="Which bot should be used",
            action="store",
            type=str)

    def test_parse_args_should_be_called(self):
        """ After setting up commands arguments must be parsed """
        parse_args(self.argparse_mock)
        self.assertTrue(self.argparse_mock.parse_args.called)

class InitChromeBrowserTestCase(TestCase):
    """ Test case for init_chrome_driver function """
    def test_(self, parameter_list):
        pass

if __name__ == "__main__":
    main()

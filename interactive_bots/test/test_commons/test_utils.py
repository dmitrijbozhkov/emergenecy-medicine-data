""" Tests for crawler utilities """
from unittest import TestCase, main
from unittest.mock import Mock, patch
from interactive_bots.commons.utils import parse_args, init_chrome_driver, open_output_file

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
    @patch("interactive_bots.commons.utils.Chrome")
    def test_init_chrome_driver_should_create_chrome_driver_if_is_headless_not_true(self, mock_driver):
        """ Chrome driver should be created if is_headless is False """
        init_chrome_driver(False)
        self.assertTrue(mock_driver.called)

    @patch("interactive_bots.commons.utils.Chrome")
    @patch("interactive_bots.commons.utils.Options")
    def test_init_chrome_driver_should_be_inicialized_with_options(self, parameter_list, mock_driver):
        """ If True passed init_chrome_driver should add chrome_options """
        options_mock = Mock()
        parameter_list.return_value = options_mock
        init_chrome_driver(True)
        mock_driver.assert_called_once_with(chrome_options=options_mock)

    @patch("interactive_bots.commons.utils.Chrome")
    @patch("interactive_bots.commons.utils.Options")
    def test_init_chrome_driver_should_be_inicialized_with_headless_option(self, parameter_list, mock_driver):
        """ If True passed init_chrome_driver should add --headless option """
        options_mock = Mock()
        parameter_list.return_value = options_mock
        init_chrome_driver(True)
        options_mock.add_argument.assert_called_once_with("--headless")

class OpenOutputFileTestCase(TestCase):
    """ Test case for open_output_file function """
    @patch("interactive_bots.commons.utils.DictWriter")
    @patch("interactive_bots.commons.utils.open")
    def test_should_open_file(self, open_mock, writer_mock):
        """ Should call open with provided path and w+ mode """
        path = "./stuff.csv"
        open_output_file(path, [1, 2, 3])
        open_mock.assert_called_once_with(path, "w+")

    @patch("interactive_bots.commons.utils.DictWriter")
    @patch("interactive_bots.commons.utils.open")
    def test_should_create_writer(self, open_mock, writer_mock):
        """ Should create DictWriter class with provided file and list of headers """
        headers = [1, 2, 3]
        file = Mock()
        open_mock.return_value = file
        open_output_file("./stuff.csv", headers)
        writer_mock.assert_called_once_with(file, headers)

    @patch("interactive_bots.commons.utils.DictWriter")
    @patch("interactive_bots.commons.utils.open")
    def test_should_return_dictionary_with_file_and_writer(self, open_mock, writer_mock):
        """ Should return dictionary with items: file and writer """
        file_ret = Mock()
        write_ret = Mock()
        open_mock.return_value = file_ret
        writer_mock.return_value = write_ret
        file = open_output_file("./stuff.csv", [1, 2, 3])
        self.assertTrue(file["file"] is file_ret, file["writer"] is write_ret)

if __name__ == "__main__":
    main()

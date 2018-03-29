""" Tests for diagnosis_online bot """
from unittest import TestCase, main
from unittest.mock import Mock
from interactive_bots.diagnosis_online_bot.bot import navigate_symptom_groups

class SymptomGroupsTestCase(TestCase):
    """ Test case for navigate, action and data function for symptom groups """

    def test_navigate_symptom_groups_should_search_for_select(self):
        """ navigate_symptom_groups should search by id for List1 """
        driver_mock = Mock()
        navigate_symptom_groups(driver_mock)
        driver_mock.find_element_by_id.assert_called_once_with("List1")

    def test_navigate_symptom_groups_should_search_for_select_options(self):
        """ navigate_symptom_groups should search within symptom group select for options """
        driver_mock = Mock()
        options_mock = Mock()
        driver_mock.find_element_by_id.return_value = options_mock
        navigate_symptom_groups(driver_mock)
        options_mock.find_elements_by_tag_name.assert_called_once_with("option")

    def test_act_symptom_groups_should_return_first_group(self):
        """ act_symptom_groups should  """
        raise NotImplementedError

if __name__ == "__main__":
    main()
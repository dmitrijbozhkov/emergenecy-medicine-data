""" Tests for diagnosis_online bot """
from unittest import TestCase, main
from unittest.mock import Mock
from selenium.common.exceptions import NoSuchElementException
from interactive_bots.diagnosis_online_bot.bot import (navigate_symptom_groups,
    act_symptom_groups,
    get_data_symptom_groups,
    navigate_symptoms,
    clear_symptoms)

class SymptomGroupsTestCase(TestCase):
    """ Test case for navigate, action and data function for symptom groups """

    def setUp(self):
        self.driver_mock = Mock()

    def test_navigate_symptom_groups_should_search_for_select(self):
        """ navigate_symptom_groups should search by id for List1 """
        navigate_symptom_groups(self.driver_mock)
        self.driver_mock.find_element_by_id.assert_called_once_with("List1")

    def test_navigate_symptom_groups_should_search_for_select_options(self):
        """ navigate_symptom_groups should search within symptom group select for options """
        options_mock = Mock()
        self.driver_mock.find_element_by_id.return_value = options_mock
        navigate_symptom_groups(self.driver_mock)
        options_mock.find_elements_by_tag_name.assert_called_once_with("option")

    def test_act_symptom_groups_should_click_first_group(self):
        """ act_symptom_groups should click on first group """
        group_mock = Mock()
        act_symptom_groups(self.driver_mock, [group_mock], 0)
        group_mock.click.assert_called_once()

    def test_act_symptom_groups_should_return_first_group_and_counter_if_acc_0(self):
        """ act_symptom_groups should return first group and 1 if acc is 0 """
        group_mock = Mock()
        symptom_act = act_symptom_groups(self.driver_mock, [group_mock], 0)
        self.assertTrue(symptom_act[0] is group_mock)
        self.assertEqual(symptom_act[1], 1)

    def test_act_symptom_groups_should_click_next_group(self):
        """ act_symptom_groups should click on group by index of counter """
        group_mock1 = Mock()
        group_mock2 = Mock()
        act_symptom_groups(self.driver_mock, [group_mock1, group_mock2], (group_mock1, 1))
        group_mock2.click.assert_called_once()

    def test_act_symptom_groups_should_return_next_group_and_counter(self):
        """ act_symptom_groups should return second group and 2 if acc counter is 1 """
        group_mock1 = Mock()
        group_mock2 = Mock()
        symptom_act = act_symptom_groups(
            self.driver_mock,
            [group_mock1, group_mock2],
            (group_mock1, 1))
        self.assertTrue(symptom_act[0] is group_mock2)
        self.assertEqual(symptom_act[1], 2)

    def test_get_data_symptom_groups_should_return_group_name(self):
        """ get_data_symptom_groups should call strip on text property of group and
        return result as dictionary """
        group_mock = Mock()
        text_mock = Mock()
        group_mock.text.strip.return_value = text_mock
        data = get_data_symptom_groups(self.driver_mock, (group_mock, 0))
        self.assertTrue(text_mock is data["symptom_group"])

class SymptomsTestCase(TestCase):
    """ Test case for navigate, action and data functions for symptoms """
    def setUp(self):
        self.driver_mock = Mock()

    def test_navigate_symptoms_should_select_symptom_wrapper(self):
        """ navigate_symptoms should element with id List2 """
        navigate_symptoms(self.driver_mock)
        self.driver_mock.find_element_by_id.assert_called_once_with("List2")

    def test_navigate_symptoms_should_select_symptom_options(self):
        """ navigate_symptoms should select all options in node with id List2 """
        options_mock = Mock()
        self.driver_mock.find_element_by_id.return_value = options_mock
        navigate_symptoms(self.driver_mock)
        options_mock.find_elements_by_tag_name.assert_called_once_with("option")

    def test_clear_symptoms_should_search_for_symptom_field(self):
        """ clear_symptoms should select element by name SelSymp[] """
        options_mock = Mock()
        remove_button = Mock()
        options_mock.find_elements_by_css_selector.return_value = []
        self.driver_mock.find_element_by_name.return_value = options_mock
        clear_symptoms(self.driver_mock, remove_button)
        self.driver_mock.find_element_by_name.assert_called_once_with("SelSymp[]")

    def test_clear_symptoms_should_select_all_options_in_symptom_field(self):
        """ clear_symptoms should get all option elements inside selSymp[] """
        options_mock = Mock()
        remove_button = Mock()
        options_mock.find_elements_by_css_selector.return_value = []
        self.driver_mock.find_element_by_name.return_value = options_mock
        clear_symptoms(self.driver_mock, remove_button)
        options_mock.find_elements_by_css_selector.assert_called_once_with("option")

    def test_clear_symptoms_should_click_on_each_symptom_and_remove_button(self):
        """ clear_symptoms should get all options in SelSymp[] and click on each of them and remove button """
        options_mock = Mock()
        remove_button = Mock()
        symptom_mock = Mock()
        options_mock.find_elements_by_css_selector.return_value = [symptom_mock]
        self.driver_mock.find_element_by_name.return_value = options_mock
        clear_symptoms(self.driver_mock, remove_button)
        symptom_mock.click.assert_called_once()
        remove_button.click.assert_called_once()

if __name__ == "__main__":
    main()
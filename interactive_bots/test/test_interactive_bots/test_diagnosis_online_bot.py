""" Tests for diagnosis_online bot """
from unittest import TestCase, main
from unittest.mock import Mock, patch
from selenium.common.exceptions import NoSuchElementException
from interactive_bots.diagnosis_online_bot.bot import (navigate_symptom_groups,
    act_symptom_groups,
    get_data_symptom_groups,
    navigate_symptoms,
    clear_symptoms,
    next_symptom_combination,
    act_symptom,
    get_data_symptom,
    navigate_diagnosis,
    act_diagnosis,
    get_data_diagnosis)

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

    def test_next_symptom_combination_should_call_next_on_acc(self):
        """ next_symptom_combination should call next on passed ExhaustOptions and pass list of symptoms in it """
        exhaust_mock = Mock()
        exhaust_mock.next.return_value = []
        symptoms_mock = [Mock()]
        button_mock = Mock()
        next_symptom_combination(symptoms_mock, exhaust_mock, button_mock)

    def test_next_symptom_combination_should_click_on_option_and_button(self):
        """ next_symptom_combination should click on each symptom and add button """
        exhaust_mock = Mock()
        symptom1_mock = Mock()
        symptom2_mock = Mock()
        exhaust_mock.next.return_value = [symptom1_mock, symptom2_mock]
        symptoms_mock = [symptom1_mock, symptom2_mock]
        button_mock = Mock()
        next_symptom_combination(symptoms_mock, exhaust_mock, button_mock)
        symptom1_mock.click.assert_called_once()
        symptom2_mock.click.assert_called_once()
        button_mock.click.assert_called()

    def test_next_symptom_combination_should_return_options(self):
        """ next_symptom_combination should return list of symptoms from next combination """
        exhaust_mock = Mock()
        options_mock = []
        exhaust_mock.next.return_value = options_mock
        symptoms_mock = [Mock()]
        button_mock = Mock()
        options = next_symptom_combination(symptoms_mock, exhaust_mock, button_mock)
        self.assertTrue(options is options_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_get_button_for_adding_symptoms(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should search for button by selector button[onclick='addfunc()'] """
        act_symptom(self.driver_mock, [Mock()], 0)
        self.driver_mock.find_element_by_css_selector.assert_any_call("button[onclick='addfunc()']")

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_get_button_for_removing_symptoms(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should search for button by selector button[onclick='delfunc()'] """
        act_symptom(self.driver_mock, [Mock()], 0)
        self.driver_mock.find_element_by_css_selector.assert_any_call("button[onclick='delfunc()']")

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_clear_symptoms(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should call clear_symptoms with driver and button for removing symptom """
        remove_mock = Mock()
        self.driver_mock.find_element_by_css_selector.side_effect = \
            lambda q: remove_mock if q == "button[onclick='delfunc()']" else Mock()
        act_symptom(self.driver_mock, [Mock()], 0)
        clear_symptoms_mock.assert_called_once_with(self.driver_mock, remove_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_call_next_symptom_combination_and_create_exhaust_options_if_acc_False(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should call next_symptom_combination
        with symptoms, ExhaustOptions and add symptom button if acc is False value """
        symptoms_mock = [Mock()]
        add_mock = Mock()
        combinations_mock = Mock()
        self.driver_mock.find_element_by_css_selector.side_effect = \
            lambda q: add_mock if q == "button[onclick='addfunc()']" else Mock()
        exhaust_mock.return_value = combinations_mock
        act_symptom(self.driver_mock, symptoms_mock, 0)
        exhaust_mock.assert_called_once_with(1)
        next_symptom_mock.assert_called_once_with(symptoms_mock, combinations_mock, add_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_return_tuple_of_symptoms_and_exhaust_options_if_acc_False(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should return Tuple with values returned from next_symptom_combination and ExhaustOptions """
        combinations_mock = Mock()
        options_mock = Mock()
        next_symptom_mock.return_value = options_mock
        exhaust_mock.return_value = combinations_mock
        result = act_symptom(self.driver_mock, [Mock()], 0)
        self.assertTrue(result[0] is options_mock)
        self.assertTrue(result[1] is combinations_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_call_next_symptom_combination_if_acc_True(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should call next_symptom_combination with list of
        symptoms, ExhaustOptions object from acc and add button if acc is True value """
        add_mock = Mock()
        acc_mock = ([Mock()], Mock())
        symptoms_mock = [Mock()]
        self.driver_mock.find_element_by_css_selector.side_effect = \
            lambda q: add_mock if q == "button[onclick='addfunc()']" else Mock()
        act_symptom(self.driver_mock, symptoms_mock, acc_mock)
        next_symptom_mock.assert_called_once_with(symptoms_mock, acc_mock[1], add_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_return_tuple_of_symptoms_and_exhaust_options_if_acc_True_value(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should returntuple of symptoms from next_symptom_combination and ExhaustOptions if acc is True """
        combinations_mock = Mock()
        acc_mock = ([Mock()], combinations_mock)
        symptoms_mock = [Mock()]
        options_mock = Mock()
        next_symptom_mock.return_value = options_mock
        result = act_symptom(self.driver_mock, symptoms_mock, acc_mock)
        self.assertTrue(result[0] is options_mock)
        self.assertTrue(result[1] is combinations_mock)

    @patch("interactive_bots.diagnosis_online_bot.bot.ExhaustOptions")
    @patch("interactive_bots.diagnosis_online_bot.bot.next_symptom_combination")
    @patch("interactive_bots.diagnosis_online_bot.bot.clear_symptoms")
    def test_act_symptom_should_return_False_if_next_symptom_combination_raises_exception(self, clear_symptoms_mock, next_symptom_mock, exhaust_mock):
        """ act_symptom should return false if next_symptom_combination raises StopIteration exception """
        next_symptom_mock.side_effect = StopIteration()
        result = act_symptom(self.driver_mock, [Mock()], 0)
        self.assertFalse(result)

    def test_get_data_symptom_should_return_dict_with_all_symptoms_as_string(self):
        """ get_data_symptom should return dictionary with 'symptoms' field with string of symptoms separated by ; """
        symptom1_mock = Mock()
        symptom2_mock = Mock()
        symptom1_text = "Зуд"
        symptom2_text = "Кашель"
        symptom1_mock.text.strip.return_value = symptom1_text
        symptom2_mock.text.strip.return_value = symptom2_text
        result = get_data_symptom(self.driver_mock, ([symptom1_mock, symptom2_mock], Mock()))
        self.assertEqual(result["symptoms"], symptom1_text + ";" + symptom2_text + ";")

class DiagnosisTestCase(TestCase):
    """ Test case for navigate, action and data functions for getting diagnosis """

    def setUp(self):
        self.driver_mock = Mock()

    def test_navigate_diagnosis_should_select_submit(self):
        """ navigate_diagnosis should select element by css selector input[type='submit'] """
        navigate_diagnosis(self.driver_mock)
        self.driver_mock.find_element_by_css_selector.assert_called_once_with("input[type='submit']")

    def test_navigate_diagnosis_should_return_from_find_element_by_css_selector(self):
        """ navigate_diagnosis should select element and return it """
        submit_mock = Mock()
        self.driver_mock.find_element_by_css_selector.return_value = submit_mock
        submit = navigate_diagnosis(self.driver_mock)
        self.assertTrue(submit is submit_mock)

    def test_act_diagnosis_should_click_submit_if_acc_False(self):
        """ act_diagnosis should call click on submit button """
        submit_mock = Mock()
        act_diagnosis(self.driver_mock, submit_mock, 0)
        submit_mock.click.assert_called_once()

    def test_act_diagnosis_should_return_True_if_acc_False(self):
        """ act_diagnosis should return True if acc is 0 """
        submit_mock = Mock()
        result = act_diagnosis(self.driver_mock, submit_mock, 0)
        self.assertTrue(result)

    def test_act_diagnosis_should_return_False_if_acc_true(self):
        """ act_diagnosis should return False if acc is True """
        submit_mock = Mock()
        result = act_diagnosis(self.driver_mock, submit_mock, True)
        self.assertFalse(result)

    @patch("interactive_bots.diagnosis_online_bot.bot.map")
    def test_get_data_diagnosis_should_select_diagnosis_field(self, map_mock):
        """ get_data_diagnosis should select element with id List11 """
        get_data_diagnosis(self.driver_mock, None)
        self.driver_mock.find_element_by_id.assert_called_once_with("List11")

    def test_get_data_diagnosis_should_select_diagnosis_options(self):
        """ get_data_diagnosis should select option elements inside node with id List11 """
        diagnoses_mock = Mock()
        diagnoses_mock.find_elements_by_css_selector.return_value = []
        self.driver_mock.find_element_by_id.return_value = diagnoses_mock
        get_data_diagnosis(self.driver_mock, None)
        diagnoses_mock.find_elements_by_css_selector.assert_called_once_with("option")

    @patch("interactive_bots.diagnosis_online_bot.bot.map")
    def test_get_data_diagnosis_should_return_map_of_stripped_text(self, map_mock):
        """ get_data_diagnosis should call map with lambda that takes text from each node and call strip on it """
        mapped_mock = Mock()
        map_mock.return_value = mapped_mock
        contents = get_data_diagnosis(self.driver_mock, None)
        self.assertEqual(contents, mapped_mock)

if __name__ == "__main__":
    main()

""" Functions for bot """
from functools import reduce
from interactive_bots.commons.utils import init_chrome_driver, ExhaustOptions
from interactive_bots.commons.form_crawler import FormActionOptions, FormCrawler
from selenium.common.exceptions import NoSuchElementException

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args.headless)
    symptom_group_action = FormActionOptions(driver)
    symptom_action = FormActionOptions(driver)

def navigate_symptom_groups(driver):
    """ Navigates through symptom body parts """
    symptom_group_select = driver.find_element_by_id("List1")
    return symptom_group_select.find_elements_by_tag_name("option")

def act_symptom_groups(driver, groups, acc):
    """ Clicks on appropriate symptom group """
    if acc == 0:
        groups[0].click()
        return (groups[0], 1)
    else:
        groups[acc[1]].click()
        return (groups[acc[1]], acc[1] + 1)

def get_data_symptom_groups(driver, group):
    """ Gets name of symptom name """
    return {"symptom_group": group[0].text.strip()}

def navigate_symptoms(driver):
    """ Navigates through symptoms """
    symptom_select = driver.find_element_by_id("List2")
    return symptom_select.find_elements_by_tag_name("option")

def clear_symptoms(driver, button):
    """ Removes all selected symptoms """
    symptom_selected = driver.find_element_by_name("SelSymp[]")
    for symptom in symptom_selected.find_elements_by_css_selector("option"):
        symptom.click()
        button.click()

def next_symptom_combination(symptoms, acc, add_symptom):
    """ Selects next sympom combination """
    options = acc.next(symptoms)
    for option in options:
        option.click()
        add_symptom.click()
    return options

def act_symptom(driver, symptoms, acc):
    """ Selects or disselects symptoms """
    add_symptom = driver.find_element_by_css_selector("button[onclick='addfunc()']")
    remove_symptom = driver.find_element_by_css_selector("button[onclick='delfunc()']")
    clear_symptoms(driver, remove_symptom)
    print(acc)
    try:
        if acc:
            options = next_symptom_combination(symptoms, acc[1], add_symptom)
            return (options, acc[1])
        else:
            acc = ExhaustOptions(len(symptoms))
            options = next_symptom_combination(symptoms, acc, add_symptom)
            return (options, acc)
    except StopIteration:
        return False

def get_data_symptom(driver, options):
    """ Gets names of symptoms """
    symptoms = reduce(lambda acc, sym: acc + sym.text.strip() + ";", options[0], "")
    return {"symptoms": symptoms}

def navigate_diagnosis(driver):
    """ Searches for submit button """
    return driver.find_element_by_css_selector("input[type='submit']")

def act_diagnosis(driver, submit, acc):
    """ Pushes submit button """
    if acc:
        return False
    else:
        submit.click()
        return True

def get_data_diagnosis(driver, acc):
    """ Get diagnoses from symptoms """
    
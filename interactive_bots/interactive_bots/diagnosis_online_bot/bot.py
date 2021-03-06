""" Functions for bot """
from functools import reduce
from interactive_bots.commons.utils import init_chrome_driver, ExhaustOptions, open_output_file
from interactive_bots.commons.form_crawler import FormActionOptions, FormCrawler

SITE_PATH = "http://www.diagnos-online.ru/symp.html"

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args)
    symptom_group_action = FormActionOptions(driver)
    symptom_action = FormActionOptions(driver)
    diagnosis_action = FormActionOptions(driver)
    symptom_group_action.set_actions(navigate_symptom_groups,
        act_symptom_groups,
        get_data_symptom_groups)
    symptom_action.set_actions(navigate_symptoms,
        act_symptom,
        get_data_symptom)
    diagnosis_action.set_actions(navigate_diagnosis,
        act_diagnosis,
        get_data_diagnosis)
    crawler = FormCrawler()
    crawler.add_action(symptom_group_action)
    crawler.add_action(symptom_action)
    crawler.add_action(diagnosis_action)
    writer = open_output_file(args.path, ["symptom_group", "symptom", "diagnosis"])
    driver.get(SITE_PATH)
    crawler.crawl(writer["writer"])
    writer["file"].close()
    driver.close()

def navigate_symptom_groups(driver):
    """ Navigates through symptom body parts """
    symptom_group_select = driver.find_element_by_id("List1")
    return symptom_group_select.find_elements_by_tag_name("option")

def act_symptom_groups(driver, groups, acc):
    """ Clicks on appropriate symptom group """
    if acc == 0:
        groups[0].click()
        return (groups[0], 1)
    if acc[1] > len(groups):
        return False
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

def next_symptom(symptoms, indexes, add_symptom):
    """ returns  """
    index = indexes.pop()
    symptoms[index].click()
    add_symptom.click()
    return symptoms[index]

def act_symptom(driver, symptoms, acc):
    """ Selects or disselects symptoms """
    add_symptom = driver.find_element_by_css_selector("button[onclick='addfunc()']")
    remove_symptom = driver.find_element_by_css_selector("button[onclick='delfunc()']")
    clear_symptoms(driver, remove_symptom)
    try:
        if acc:
            symptom = next_symptom(symptoms, acc[0], add_symptom)
            return (acc[0], symptom)
        else:
            symptom_indexes = [x for x in range(len(symptoms))]
            symptom = next_symptom(symptoms, symptom_indexes, add_symptom)
            return (symptom_indexes, symptom)
    except IndexError:
        return False

def get_data_symptom(driver, options):
    """ Returns record with selected symptom """
    return {"symptom": options[1].text.strip()}

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
    diagnosis_field = driver.find_element_by_id("List11")
    diagnoses = diagnosis_field.find_elements_by_css_selector("option")
    return map(lambda d: {"diagnosis": d.text.strip()}, diagnoses)

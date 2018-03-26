""" Functions for bot """
from interactive_bots.commons.utils import init_chrome_driver

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args.headless)
    return

def navigate_symptom_groups(driver):
    """ Navigates through symptom body parts """
    symptom_group_select = driver.find_element_by_id("List1")
    return symptom_group_select.find_elements_by_tag_name("option")

def act_symptom_groups(driver, groups, index):
    """ Clicks on appropriate symptom group """
    groups[index].click()
    return groups[index]

def get_data_symptom_groups(driver, group):
    """ Gets name of symptom name """
    return group.text.strip()

def navigate_symptoms(driver):
    """  """
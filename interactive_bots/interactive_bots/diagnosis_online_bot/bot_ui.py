""" Functions for working with ui elements """

def get_symptom_groups(driver):
    """ Selects symptom groups on site ui """
    return driver.find_elements_by_css_selector("#List1 option")

def get_symptoms(driver):
    """ Selects symptoms on site ui """
    return driver.find_elements_by_css_selector("#List2 option")

def get_selected_symptoms(driver):
    """ Selects selected symptoms """
    return driver.find_elements_by_css_selector("select[name='SelSymp[]'] option")

def get_diagnosis(driver):
    """ Selects result diagnosis """
    return driver.find_elements_by_css_selector("#List11 option")

def get_buttons(driver):
    """ Selects buttons for adding symptom and analyzing them """
    return {
        "add": driver.find_element_by_css_selector("button[onclick='addfunc()']"),
        "analyze": driver.find_element_by_css_selector("input[type='submit']")
    }

def get_remove_button(driver):
    """ Selects button for removing symptom """
    return driver.find_element_by_css_selector("button[onclick='delfunc()']")

def clear_symptoms(symptoms, button):
    """ Removes all selected symptoms """
    for symptom in symptoms:
        symptom.click()
        button.click()

def scrape_diagnosis(driver):
    """ Performs actions for scraping data from symptom analyzing ui """
    symptom_groups = get_symptom_groups(driver)
    symptom_group_pointer = 0
    symptoms_pointer = 0
    while symptom_group_pointer < len(symptom_groups):
        buttons = get_buttons(driver)
        symptom_groups[symptom_group_pointer].click()
        symptoms = get_symptoms(driver)
        symptoms[symptoms_pointer].click()
        buttons["add"].click()
        buttons["analyze"].click()
        symptom_groups = get_symptom_groups(driver)
        symptom_groups[symptom_group_pointer].click()
        symptoms = get_symptoms(driver)
        yield {
            "diagnosis": get_diagnosis(driver),
            "symptom_group": symptom_groups[symptom_group_pointer],
            "symptom": symptoms[symptoms_pointer]
        }
        clear_symptoms(get_selected_symptoms(driver), get_remove_button(driver))
        symptoms_pointer += 1
        if symptoms_pointer >= len(symptoms):
            symptom_group_pointer += 1
            symptoms_pointer = 0

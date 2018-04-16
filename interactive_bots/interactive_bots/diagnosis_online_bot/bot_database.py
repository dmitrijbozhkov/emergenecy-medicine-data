""" Functions for working with sqlite database """
import sqlite3

def connect_database(args):
    """ Connect do database by command line arguments """
    return sqlite3.connect(args.path)

def prepare_database(args):
    """ Prepears database tables """
    connection = connect_database(args)
    create_cursor = connection.cursor()
    scema = ""
    with open(args.scema, "r") as file:
        scema = file.read()
    for command in scema.split("\n\n"):
        create_cursor.execute(command)
    connection.commit()
    connection.close()

def scrape_complete(connection, driver):
    """ Commits changes, closes database connection and closes driver """
    connection.commit()
    connection.close()
    driver.close()

def update_complete(connection):
    """ Commits changes after updating descriptions """
    connection.commit()
    connection.close()

def fetch_diagnoses(cursor):
    """ Returns list of diagnoses """
    cursor.execute("""SELECT * FROM diagnosis""")
    return cursor.fetchall()

def update_description(cursor, row):
    """ Sets description contents instead of link """
    cursor.execute("""UPDATE diagnosis SET description=? WHERE name=?""", (row[1], row[0]))

def database_writer(cursor, data):
    """ Writes diagnosis data """
    check_template = """SELECT EXISTS(SELECT * FROM {0} WHERE name=?)"""
    insert_template = """INSERT INTO {0} {1} VALUES {2}"""
    group_check = cursor.execute(check_template.format("symptom_group"),
                                 (data["symptom_group"],)).fetchall()
    symptom_check = cursor.execute(check_template.format("symptom"),
                                   (data["symptom"],)).fetchall()
    if not group_check[0][0]:
        cursor.execute(insert_template.format("symptom_group", "(name)", "(?)"),
                       (data["symptom_group"],))
    if not symptom_check[0][0]:
        cursor.execute(insert_template.format("symptom", "(name, group_name)", "(?, ?)"),
                       (data["symptom"], data["symptom_group"]))
    for diagnosis in data["diagnosis"]:
        diag_check = cursor.execute(check_template.format("diagnosis"),
                                    (diagnosis[0],)).fetchall()
        if not diag_check[0][0]:
            cursor.execute(insert_template.format("diagnosis", "(name, description)", "(?, ?)"),
                           (diagnosis[0], diagnosis[2]))
        cursor.execute(insert_template.format("symptom_diagnosis", "(symptom_name, diagnosis_name, symptom_group_name, probability)", "(?, ?, ?, ?)"),
                       (data["symptom"], diagnosis[0], data["symptom_group"], diagnosis[1]))

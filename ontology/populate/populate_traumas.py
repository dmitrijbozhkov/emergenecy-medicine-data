""" Adds traumas to ontology """
import sqlite3

TRAUMA_DATABASE = "./database/trauma_scema.sql"

def create_trauma_database(path):
    """ Creates trauma database scema """
    connection = sqlite3.connect(path)
    create_cursor = connection.cursor()
    scema = ""
    with open(TRAUMA_DATABASE, "r") as file:
        scema = file.read()
    for command in scema.split("\n\n"):
        create_cursor.execute(command)
    connection.commit()
    connection.close()

def 

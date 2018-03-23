""" Common utilities for bots """
from csv import writer
from argparse import ArgumentParser

def parse_params():
    """ Parses passed folder path for bots output files and if browser should be in headless mode """
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", required=True)
    parser.add_argument("-h", "--headless", required=False)
    return parser.parse_args

def create_writer(folder, name):
    """ Creates csv file writer """
    file = open(folder + name, "w+")
    write = writer(file)
    return {
        "file": file,
        "writer": write
    }
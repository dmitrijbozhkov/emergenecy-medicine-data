""" Startup operations """
from argparse import ArgumentParser

def parse_sites(args):
    """ Zips path to their data folders and crawlers """


def run():
    """ Runs application """
    ap = ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="Path to web resource")
    ap.add_argument("-f", "--data-folder", help="Folder for storing data")
    ap.add_argument("-l", "--logging", help="Log file location, if nothing provided then logs will be in stdout")
    ap.add_argument("-d", "--driver", required=True, help="Type of driver required for site")
    
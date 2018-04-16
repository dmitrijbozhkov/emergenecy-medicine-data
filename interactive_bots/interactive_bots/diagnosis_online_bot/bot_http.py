""" Functions for working with http """
import re
from functools import reduce
from bs4 import BeautifulSoup
import requests

DESEASE_LINK = "http://www.diagnos-online.ru/zabolevaniya.html"

def parse_page(url):
    """ Decode and parse site page """
    response = requests.get(url)
    page = response.content.decode("windows-1251", "ignore")
    return BeautifulSoup(page, "html.parser")

def get_description_links():
    """ Returns list of desease description links """
    bs = parse_page(DESEASE_LINK)
    return bs.select("div.submen a")

def match_link(links, name):
    """ Diagnoses in app have substrings of how diagnosis named in desease list """
    keys = links.keys()
    for k in keys:
        if k.lower() in name.lower():
            return links[k]
    return ""

def request_description(data):
    """ Returns descriptions for desease links """
    regex = re.compile(r"\w+")
    if data[1]:
        soup = parse_page(data[1])
        data = (data[0],
                reduce(lambda a, v: a + str(v), soup.find_all(["p", "h2"], string=regex), ""))
    return data

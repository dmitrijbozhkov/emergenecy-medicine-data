""" Bot written using reactivex """
import multiprocessing
from functools import partial
from rx import Observable
from rx.concurrency import ThreadPoolScheduler
from rx.core import Scheduler
from interactive_bots.commons.utils import init_chrome_driver
from interactive_bots.diagnosis_online_bot.bot_ui import scrape_diagnosis
from interactive_bots.diagnosis_online_bot.bot_http import (get_description_links,
                                                            match_link,
                                                            request_description)
from interactive_bots.diagnosis_online_bot. bot_database import (database_writer,
                                                                 scrape_complete,
                                                                 prepare_database,
                                                                 connect_database,
                                                                 update_description,
                                                                 update_complete,
                                                                 fetch_diagnoses,)

SITE_PATH = "http://www.diagnos-online.ru/symp.html"

def run(args):
    """ Sets up and runs bot """
    driver = init_chrome_driver(args)
    prepare_database(args)
    driver.get(SITE_PATH)
    connection = connect_database(args)
    scrape_ui(driver, connection)
    print("Scraping completed")
    connection = connect_database(args)
    optimal_thread_count = multiprocessing.cpu_count() + 1
    scheduler = ThreadPoolScheduler(optimal_thread_count)
    update_descriptions(connection, scheduler)
    scheduler.executor.shutdown()
    print("Comlete!")

def scrape_ui(driver, connection):
    """ Scrapes ui of application and records """
    cursor = connection.cursor()
    links = Observable.from_(get_description_links()) \
        .skip(9) \
        .to_dict(lambda e: e.string, lambda e: "http://www.diagnos-online.ru/" + e["href"])
    scraped_data = Observable.from_(scrape_diagnosis(driver)) \
        .map(lambda e: {
            "diagnosis": [(d.text.split("    ")[1], float(d.text.split("    ")[0][:-1])) for d in e["diagnosis"]],
            "symptom_group": e["symptom_group"].text.strip(),
            "symptom": e["symptom"].text.strip()
        })
    wait_links = Observable.concat(links, scraped_data).skip(1)
    Observable.combine_latest(wait_links, links, lambda d, l: {
        "diagnosis": [(i[0], i[1], match_link(l, i[0])) for i in d["diagnosis"]],
        "symptom_group": d["symptom_group"],
        "symptom": d["symptom"]
    }) \
        .do_action(print) \
        .subscribe(on_next=partial(database_writer, cursor),
                   on_completed=partial(scrape_complete, connection, driver))

def update_descriptions(connection, scheduler):
    """ Updates desease links to description contents """
    cursor = connection.cursor()
    diagnosis_info = Observable.from_(fetch_diagnoses(cursor)) \
        .flat_map(lambda i: Observable.just(request_description(i))) \
        .do_action(print) \
        .subscribe(on_next=partial(update_description, cursor),
                   on_completed=partial(update_complete, connection))

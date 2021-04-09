#!/usr/bin/env python3

import os
import logging
import json
from time import sleep
from owlpy import generateId, latest_obs, lookup_checklist
from datetime import datetime, timedelta
from geopy.geocoders import GoogleV3
from twisted.internet import task, reactor

LAT = "45.1497889"
LNG = "-93.3602303"

EBIRD_API_TOKEN = os.getenv('EBIRD_API_TOKEN')


def check_owl(owl):
    latest_results = latest_obs(api_token=EBIRD_API_TOKEN, species_code=owl, lat=LAT, lng=LNG)
    for result in latest_results:
        log.debug(f"found sighting: {owl} - {result['locName']} - {result['obsDt']}")
    print(latest_results)
    write_file(latest_results)

# def handle_new_sighting(id, data, owl):
#     obs_data = lookup_checklist(data['subId'], EBIRD_API_TOKEN, owl)
#     log.info("%s is a new sighting!  Inserting in database and alerting Holden!" % id)
#     log.info(f"Sighting Location Name: {data['locName']}")
#     log.info(f"Sighting Address: {data['address']}\nSighting Time: {data['obsDt']}")
#     log.info(f"Spotted By: {obs_data['observer_name']}")
#     if obs_data['comments']:
#         log.info(f"Notes: {obs_data['comments']}")
#     data.update(obs_data)
#     cb.upsert_couchbase(id, data)
#     sleep(1)

def write_file(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
    log = logging.getLogger(__name__)
    check_owl("nswowl")
    sleep(1)
    # check_owl("loeowl")
    # sleep(1)
    # check_owl("snoowl1")
    # sleep(1)
    # check_owl("easowl1")

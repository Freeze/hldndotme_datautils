#!/usr/bin/env python3.8

import os
import logging
import json
import holdenPy
from time import sleep
from owlpy import generateId, latest_obs, lookup_checklist
from datetime import datetime, timedelta
from geopy.geocoders import GoogleV3
from twisted.internet import task, reactor

LAT = "45.1497889"
LNG = "-93.3602303"
OWL_DATA_PATH = '/var/www/html/data.json'
SPECIES_LIST = ["nswowl", "loeowl", "snoowl1", "easowl1"]
TESTING_LIST = ['brdowl']

EBIRD_API_TOKEN = os.getenv('EBIRD_API_TOKEN')


def check_owl(owl):
    latest_results = latest_obs(api_token=EBIRD_API_TOKEN, species_code=owl, lat=LAT, lng=LNG)
    for result in latest_results:
        log.debug(f"found sighting: {owl} - {result['locName']} - {result['obsDt']}")
    return latest_results


if __name__ == "__main__":
    logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
    log = logging.getLogger(__name__)
    for owl in TESTING_LIST:
        log.info(f'Checking {owl} sightings!')
        sighting_list = []
        owl_path = f'/var/www/html/{owl}.json'
        results = check_owl(owl)
        for result in results:
            sighting_list.append(result)
        sleep(1)
        sighting_light = sorted(sighting_list, key=lambda k: k['daysAgo'])
        holdenPy.write_json(owl_path, sighting_list)
        log.info(f'Finished checking {owl} sightings!  Moving on...')
    log.info('Finished checking all species.  Moving on.')

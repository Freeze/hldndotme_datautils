import logging
import requests
from datetime import datetime, timedelta
from geopy.geocoders import GoogleV3
import os


EBIRD_API_BASE_URL = "https://api.ebird.org/v2"
GOOGLE_API_TOKEN = os.getenv('GOOGLE_TOKEN')
log = logging.getLogger(__name__)
geolocator = GoogleV3(api_key=GOOGLE_API_TOKEN)

def latest_obs(api_token, species_code, lat, lng):
    url = "%s/data/obs/geo/recent/%s?lat=%s&lng=%s&dist=50" % (EBIRD_API_BASE_URL, species_code, lat, lng)
    headers = {
        "X-eBirdApiToken": api_token
    }
    response = requests.request("GET", url, headers=headers)
    eBirdJsonResponse = response.json()
    for sighting in eBirdJsonResponse:
        log.info(f"Found {species_code} sighting at {sighting['locName']}")
        days_ago = calculate_time_difference(sighting)
        sighting_address = geolocator.reverse(f"{sighting['lat']}, {sighting['lng']}")
        sighting.update({'daysAgo': days_ago})
        try:
            sighting.update({'address': str(sighting_address[0])})
            sighting.update({'city': str(sighting_address[2])})
        except:
            sighting.update({'address': str(sighting_address)})
            sighting.update({'city': str(sighting_address)})
    return eBirdJsonResponse


def calculate_time_difference(sighting):
    sightingDtObj = datetime.strptime(sighting['obsDt'], '%Y-%m-%d %H:%M')
    currentTime = datetime.now()
    dtDiff = currentTime - sightingDtObj
    daysAgo = divmod(dtDiff.total_seconds(), 86400)[0]
    return daysAgo


def lookup_checklist(checklist_id, api_token, species_code):
    return_dict = {}
    url = f"{EBIRD_API_BASE_URL}/product/checklist/view/{checklist_id}"
    headers = {
        "X-eBirdApiToken": api_token
    }
    response = requests.get(url, headers=headers).json()
    for entry in response['obs']:
        if entry['speciesCode'] == species_code:
            return_dict['comments'] = entry.get('comments', None)
    return_dict['observer_name'] = response['userDisplayName']
    return return_dict
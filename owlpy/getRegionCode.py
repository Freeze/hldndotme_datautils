#!/usr/bin/env python3
"""
# provide latitude & longitude, return eBird "regionCode"
Written by Jess Sullivan
@ https://transscendsurvival.org/
available at:
https://raw.githubusercontent.com/Jesssullivan/GIS_Shortcuts/master/regioncodes.py
"""
import requests
import json

def getRegionCode(lat, lon):

    # this municipal api is a publicly available, no keys needed afaict
    census_url = str('https://geo.fcc.gov/api/census/area?lat=' +
                     str(lat) +
                     '&lon=' +
                     str(lon) +
                     '&format=json')

    # send out a GET request:
    payload = {}
    get = requests.request("GET", census_url, data=payload)

    # parse the response, all api values are contained in list 'results':
    response = json.loads(get.content)['results'][0]

    # use the last three digits from the in-state fips code as the "subnational 2" identifier:
    fips = response['county_fips']

    # assemble and return the "subnational type 2" code:
    regioncode = 'US-' + response['state_code'] + '-' + fips[2] + fips[3] + fips[4]
    print('formed region code: ' + regioncode)
    return regioncode


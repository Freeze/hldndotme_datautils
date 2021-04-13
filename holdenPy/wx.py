import os
import requests
import json


def get_afd(wfo):
    product_list = f"https://api.weather.gov/products/types/afd/locations/{wfo}"
    url = product_list['@graph'][0]['@id']
    return requests.get(url).json()

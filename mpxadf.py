#!/usr/bin/env python3.8
import os
import requests
import json
import holdenPy
from gtts import gTTS

LANG = 'en'

if __name__ == "__main__":
    response = requests.request("GET", URL, headers=headers)
    latest_afd = response.json()['@graph'][0]['@id']
    afd_txt = requests.request("GET", latest_afd, headers=headers)
    afd_json = afd_txt.json()
    my_text = afd_json['productText']
    #write_json('/var/www/html/afd.json', afd_json)
    # ttsobj = gTTS(text=mytext, lang=LANG, slow=False)
    # ttsobj.save("welcome.mp3")

#!/usr/bin/env python3.8
import os
import json


def read(path):
    try:
        db = open(path, "r")
    except Exception as e:
        print(e)
        if not os.path.isfile(path):
            db = open(path, "w")
            db.close()
        try:
            data = json.load(db)
            db.close()
            return data
        except Exception as e:
            print(e)
            return []


barred_owls = read('/var/www/html/brdowl.json')
print(type(barred_owls))
print(barred_owls)

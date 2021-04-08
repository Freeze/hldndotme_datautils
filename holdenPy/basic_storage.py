import json
import os
import logging

file_name = "data.json"
log = logging.getLogger(__name__)


def check_db(name=file_name):
    if not os.path.isfile(name):
        log.info("Creating database now!")
        db = open(name, "w")
        db.close()


def read_db():
    try:
        db = open(file_name, "r")
    except:
        log.info("Database not found.")
        check_db()
        read_db()
    try:
        data = json.load(db)
        db.close()
        return data
    except:
        return []


def update_db_old(key, value):
    data = read_db()
    data.update({key: value})
    db = open(file_name, "w")
    json.dump(data, db)
    db.close()


def update_db(value):
    data = read_db()
    data.append(value)
    db = open(file_name, "w")
    json.dump(data, db)
    db.close()

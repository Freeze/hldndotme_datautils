from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
from couchbase.exceptions import DocumentNotFoundException
import time
import requests
import random


class Couchbase:
    def __init__(self, **kwargs):
        self.init_connection(kwargs)

    def init_connection(self, args):
        global couchbase_connection
        connection_string = 'couchbase://%s' % (args['server'])
        couchbase_cluster = Cluster(connection_string, ClusterOptions(PasswordAuthenticator(args['username'], args['password'])))
        couchbase_bucket = couchbase_cluster.bucket(args['bucket'])
        self.bucket_name = args['bucket']
        self.couchbase_connection = couchbase_bucket.default_collection()

    def query_owl(self, owl):
        try:
            query = f'SELECT * FROM `owlert` WHERE `speciesCode` = "{owl}"'
            result_list = []
            for result in self.couchbase_connection.query(query):
                print(result)
                result_list.append(result)
        except Exception as e:
            print(e)

    def get_previous_sightings(self, owl):
        try:
            known_sightings = []
            query = f'SELECT RAW META().id FROM `owlert` WHERE `speciesCode` = "{owl}"'
            results = self.couchbase_connection.query(query)
            for result in results:
                known_sightings.append(result)
            return known_sightings
        except Exception as e:
            print(e)

    def upsert_couchbase(self, id, data):
        try:
            self.couchbase_connection.upsert(id, data)
        except Exception as e:
            print(e)

    def get_doc(self, key):
        try:
            result = self.couchbase_connection.get(key)
            return result.content
        except DocumentNotFoundException:
            self.upsert_couchbase(key, {})

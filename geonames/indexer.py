from elasticsearch import Elasticsearch
from datetime import datetime


def es_index(data):
    data['timestamp'] = datetime.now()
    es = Elasticsearch()
    print es.index(index="geonames", doc_type="geonames", id=data['geonameid'], body=data)

def es_suggest(data):
    data['timestamp'] = datetime.now()
    es = Elasticsearch()
    print data

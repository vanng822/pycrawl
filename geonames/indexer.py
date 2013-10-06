from elasticsearch import Elasticsearch
from datetime import datetime
import threading
local_data = threading.local()

def get_es():
    try:
        es = local_data.es
    except:
        es = Elasticsearch()
        local_data.es = es
    #print id(es)
    return es
    
def es_index(data):
    data['timestamp'] = datetime.now()
    es = get_es()
    es.index(index='geonames', doc_type='geonames', id=data['geonameid'], body=data)

def es_suggest(data):
    data['timestamp'] = datetime.now()
    #es = Elasticsearch()
    print data

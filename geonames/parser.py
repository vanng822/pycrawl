

import threading
import time
import argparse
import Queue
import codecs
from datetime import datetime

def to_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()

geoname_fields = (
    ('geonameid',int)         ,#: integer id of record in geonames database
    ('name', unicode)              ,#: name of geographical point (utf8) varchar(200)
    ('asciiname', unicode)         ,#: name of geographical point in plain ascii characters, varchar(200)
    ('alternatenames', unicode)    ,#: alternatenames, comma separated varchar(5000)
    ('latitude', float)          ,#: latitude in decimal degrees (wgs84)
    ('longitude', float)         ,#: longitude in decimal degrees (wgs84)
    ('feature_class', unicode)     ,#: see http://www.geonames.org/export/codes.html, char(1)
    ('feature_code', unicode)      ,#: see http://www.geonames.org/export/codes.html, varchar(10)
    ('country_code', unicode)      ,#: ISO-3166 2-letter country code, 2 characters
    ('cc2', unicode)              ,#: alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
    ('admin1_code', unicode)       ,#: fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    ('admin2_code', unicode)       ,#: code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    ('admin3_code', unicode)       ,#: code for third level administrative division, varchar(20)
    ('admin4_code', unicode)       ,#: code for fourth level administrative division, varchar(20)
    ('population', int)        ,#: bigint (8 byte int) 
    ('elevation', int)         ,#: in meters, integer
    ('dem', int)               ,#: digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    ('timezone', unicode) ,#: the timezone id (see file timeZone.txt) varchar(40)
    ('modification_date', to_date)
)

zip_fields = (
    ('country_code', unicode)      ,#: iso country code, 2 characters
    ('postal_code', unicode)       ,#: varchar(20)
    ('place_name', unicode)        ,#: varchar(180)
    ('admin_name1', unicode)       ,#: 1. order subdivision (state) varchar(100)
    ('admin_code1', unicode)       ,#: 1. order subdivision (state) varchar(20)
    ('admin_name2', unicode)       ,#: 2. order subdivision (county/province) varchar(100)
    ('admin_code2', unicode)       ,#: 2. order subdivision (county/province) varchar(20)
    ('admin_name3', unicode)       ,#: 3. order subdivision (community) varchar(100)
    ('admin_code3', unicode)       ,#: 3. order subdivision (community) varchar(20)
    ('latitude', float)          ,#: estimated latitude (wgs84)
    ('longitude', float)         ,#: estimated longitude (wgs84)
    ('accuracy', float)          #: accuracy of lat/lng from 1=estimated to 6=centroid
)

def read_worker(filename, queue):
    print 'start read_worker'
    fp = codecs.open(filename, "r", "utf-8")
    if not fp:
        raise Exception('Could not open file')
    
    line = fp.readline()
    while line != '':
        queue.put_nowait(line)
        line = fp.readline()

def process_worker(queue, callback):
    print 'start process_worker'
    ## give read worker sometimes to build up the queue
    time.sleep(0.5)
    q_full = True
    tries = 1
    max_tries = 3
    fields = None
    while q_full:
        try:
            line = queue.get(True, timeout=1)
            line = line.strip()
            line = line.split("\t")
            if fields is None:
                if len(line) == len(geoname_fields):
                    fields = geoname_fields
                elif len(line) == len(zip_fields):
                    fields = zip_fields
                else:
                    raise Exception('Not supported geoname data')
                
            data = {}
            for index, field in enumerate(fields):
                try:
                    # try to convert to the defined type, if failed convert to string
                    data[field[0]] = field[1](line[index])
                except:
                    data[field[0]] = unicode(line[index])
            
            if callback:
                callback(data)
            else:
                print 'No callback. Printing data'
                print data
        except Queue.Empty:
            print 'q empty'
            if tries > max_tries:
                q_full = False
            else:
                tries += 1
                time.sleep(1)


def main(args):
    
    if args.callback is not None:
        callback = args.callback.split(':')
        if len(callback) == 2:
            module = __import__(callback[0])
            m_namespaces = callback[0].split('.')
            for index in range(1,len(m_namespaces)):
                module = getattr(module, m_namespaces[index])
            callback = getattr(module, callback[1])
            if not callable(callback):
                raise Exception('Callback is not callable')
        else:
            raise Exception('Invalid callback')
    else:
        callback = None
   
    q = Queue.Queue()
   
    rt = threading.Thread(target=read_worker, args = (args.filename, q, ))
    rt.start()
         
    for i in range(args.num_workers):
        t = threading.Thread(target = process_worker, args = (q, callback, ))
        t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parsing geonames database text file. Make a callback with each row (dictionary) as argument')
    parser.add_argument('-f', '--filename', required=True,
                   help='path to file containing geoname data. See http://download.geonames.org/export/dump/')
    parser.add_argument('-n', '--num_workers', required=False, type=int, default=10,
                   help='Number of workers. Default is 10')
    parser.add_argument('-c', '--callback', required=False, default=None,
                   help='Function to process each row, example geonames.indexer:es_index')
    args = parser.parse_args()
    
    main(args)
    
    
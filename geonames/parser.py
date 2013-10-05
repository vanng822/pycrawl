

import threading
import time
import argparse
import Queue
import codecs

fields = [
    'geonameid'         ,#: integer id of record in geonames database
    'name'              ,#: name of geographical point (utf8) varchar(200)
    'asciiname'         ,#: name of geographical point in plain ascii characters, varchar(200)
    'alternatenames'    ,#: alternatenames, comma separated varchar(5000)
    'latitude'          ,#: latitude in decimal degrees (wgs84)
    'longitude'         ,#: longitude in decimal degrees (wgs84)
    'feature_class'     ,#: see http://www.geonames.org/export/codes.html, char(1)
    'feature_code'      ,#: see http://www.geonames.org/export/codes.html, varchar(10)
    'country_code'      ,#: ISO-3166 2-letter country code, 2 characters
    'cc2'               ,#: alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
    'admin1_code'       ,#: fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    'admin2_code'       ,#: code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80) 
    'admin3_code'       ,#: code for third level administrative division, varchar(20)
    'admin4_code'       ,#: code for fourth level administrative division, varchar(20)
    'population'        ,#: bigint (8 byte int) 
    'elevation'         ,#: in meters, integer
    'dem'               ,#: digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    'timezone'          ,#: the timezone id (see file timeZone.txt) varchar(40)
    'modification_date'
]

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
    while q_full:
        try:
            line = queue.get(True, timeout=1)
            line = line.strip()
            line = line.split("\t")
            if len(line) != len(fields):
                print 'line error'
                continue
            
            data = {}
            for index, field in enumerate(fields):
                data[field] = unicode(line[index])
            
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
    q = Queue.Queue()
    rt = threading.Thread(target=read_worker, args = (args.filename, q, ))
    rt.start()
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
        
    for i in range(args.num_workers):
        t = threading.Thread(target = process_worker, args = (q, callback, ))
        t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename', required=True,
                   help='path to file containing cities')
    parser.add_argument('-n', '--num_workers', required=False, type=int, default=10,
                   help='Number of workers. Default is 10')
    parser.add_argument('-c', '--callback', required=False, default=None,
                   help='Function to process each row')
    args = parser.parse_args()
    
    main(args)
    
    
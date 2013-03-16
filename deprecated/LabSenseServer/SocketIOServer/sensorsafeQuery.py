import sys
import httplib, urllib
import json
import time
import datetime
SERVER_ADDRESS = '128.97.93.29'
SERVER_PREFIX = ''
HTTP_REQUEST_TIMEOUT = 600
API_KEY = "ff5ee3d50ff218c83b5b6fdfc28eef65aeb430fe"
# Here are some example queries
#message = { 'query': {} } # get all data
#message = { 'query': { 'data_channel': { '$in': [ 'ECG', 'AccelerometerX' ] } } } # get data with data_channel ECG or AccelerometerX
message = { 'query': { 'data_channel': 'Raritan_Current_1', 'timestamp': { '$gte': int(round(time.time()) * 1000)-10000, "$lte": int(time.time()*1000) } } }  # get data with data_channel ECG or AccelerometerX
#message = { 'query': { 'data_channel': { '$in': [ 'Raritan_Current_1' ] } } }
#message =  { 'query': { 'data_channel': 'Raritan_Current_1' } }
#message = { 'query': { 'data_channel': 'ECG' } } # get data with data_channel ECG
#message = { 'query': { 'timestamp': { '$gte': 10, '$lte': 1317163451103 } } }
#message = { 'query': {}, 'distinct': 'location' } # get distinct locations
#message = { 'query': {}, 'at': 'first' } # get the first data
#message = { 'query': {}, 'at': 'last' } # get the last data
#message = { 'query': {}, 'at': 1 } # get 2nd data (index start with 0)
#message = { 'query': {}, 'limit': 1 } # get only 1 data
# They are basically mongoDB query language.  You can learn more about the language at  http://www.mongodb.org/display/DOCS/Querying
try:
        params = urllib.urlencode({'apikey': API_KEY, 'data': json.dumps(message)})  
        
        conn = httplib.HTTPSConnection(SERVER_ADDRESS, timeout=HTTP_REQUEST_TIMEOUT)
        conn.request('POST', SERVER_PREFIX + '/query/', params)
        
        response = conn.getresponse()
        print response.status, response.reason
        print response.getheaders()
        reply = response.read()
        print reply
        conn.close()
except Exception as detail:
        print 'Error:', detail

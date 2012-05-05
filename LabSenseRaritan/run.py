import sqlite3
import os
import json
import sys, struct
import time

import raritan
from waveseg import *
import upthread

#RARITAN_IP_ADDRESS = '131.179.144.242'
RARITAN_IP_ADDRESS = '172.17.5.179'

SAMPLE_INTERVAL = 0.1
MAX_NUM_VALUEBLOB = 5

upload_thread = None

# sqlite3 databse
waveseg_db = None

# WaveSeg for each 8 channels
waveseg_buf = []

# SENSOR DEPENDENT WSS IDs
def init_waveseg_buf():
    global waveseg_buf
    waveseg_buf.append(WaveSeg(wss_id=28))
    waveseg_buf.append(WaveSeg(wss_id=12))
    waveseg_buf.append(WaveSeg(wss_id=14))
    waveseg_buf.append(WaveSeg(wss_id=15))
    waveseg_buf.append(WaveSeg(wss_id=16))
    waveseg_buf.append(WaveSeg(wss_id=17))
    waveseg_buf.append(WaveSeg(wss_id=18))
    waveseg_buf.append(WaveSeg(wss_id=19))

def init_db():
	global waveseg_db
	waveseg_db = sqlite3.connect(upthread.DB_FILENAME)

	c = waveseg_db.cursor()
	try:
		c.execute('DROP TABLE WaveSeg')
	except:
		pass
	
	c.execute('CREATE TABLE WaveSeg (ID INTEGER PRIMARY KEY, UploadTime TEXT, WaveSegSeriesID INTEGER, StartTime REAL, SamplingInterval REAL, StaticLocation TEXT, ValueBlob TEXT)')

	'''
	t = (None, None, 1, 1, 1, "[ 1, 2, 3 ]", "[ 4, 5, 6 ]")
	c.execute('insert into WaveSeg values (?, ?, ?, ?, ?, ?, ?)', t)
	'''

	'''
	c.execute('INSERT INTO WaveSeg VALUES (\
				NULL,\
				NULL,\
				1,\
				1263274033.812,\
				3.0,\
				"[ 34.0132641, -118.4165829, null ]",\
				"[ [null, null, null, null, 1, 2, 3, 4, 5], [null, null, null, null, 2, 3, 4, 5, 6], [null, null, null, null, 3, 4, 5, 6, 7] ]")'
			)
	c.execute('INSERT INTO WaveSeg VALUES (\
				NULL,\
				NULL,\
				1,\
				1263274033.812,\
				3.0,\
				"[ 34.0132641, -118.4165829, null ]",\
				"[ [null, null, null, null, 1, 2, 3, 4, 5], [null, null, null, null, 2, 3, 4, 5, 6], [null, null, null, null, 3, 4, 5, 6, 7] ]")'
			)
	'''

	waveseg_db.commit()
	c.close()

# SENSOR DEPENDENT FUNTION
def update_waveseg_buf(timestamp, data):
    global waveseg_buf

    #print 'update...'
    for i, cur_waveseg in enumerate(waveseg_buf):
        cur_waveseg.value_blob.append([timestamp, None, None, None, data[0+i], data[8+i], data[16+i], data[24+i], data[32+i]])

def store_waveseg_buf():
	global waveseg_buf

	print 'storing data...'

	cur = waveseg_db.cursor()
	for cur_waveseg in waveseg_buf:
		cur.execute('INSERT INTO WaveSeg VALUES (?,?,?,?,?,?,?)', cur_waveseg.get_db_tuple())
	waveseg_db.commit()
	cur.close()

	# notify upload thread
	upload_thread.data_ready()

def clean_up():
    global waveseg_db
    print
    print 'closing...'
    waveseg_db.close()
    upload_thread.stop()
    upload_thread.data_ready()
    upload_thread.join()

def main():
    global upload_thread		

    init_db()
    init_waveseg_buf()
    upload_thread = upthread.UploadThread()
    upload_thread.start()
    
    while True:

        # Retreive data from Raritan
        data = raritan.Get(RARITAN_IP_ADDRESS)
        #data = [0, 0, 0, 0, 0, 0, 0, 0, 121000, 121000, 121000, 121000, 121000, 121000, 121000, 121000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        timestamp = time.time()
        
        print data
        if len(data) != 40:
	    	print 'Error from raritan: %s'%data
	    	continue

        # collect data in buffer ...
        update_waveseg_buf(timestamp, data)

        # Store waveseg_buf into local database
        if len(waveseg_buf[0].value_blob) >= MAX_NUM_VALUEBLOB:
            store_waveseg_buf()

            # empty value_blobs in waveseg_buf
            for cur_waveseg in waveseg_buf:
                cur_waveseg.value_blob = []

        # sleep ...
        time.sleep(SAMPLE_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clean_up()


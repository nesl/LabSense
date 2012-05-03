import httplib
import time
import sqlite3
import threading
import os

from waveseg import *

DB_FILENAME = './waveseg_db' # if android, will be changed in main()

#SERVER_ADDRESS = '192.168.0.10'
#SERVER_ADDRESS = '128.97.93.26'
SERVER_ADDRESS = '128.97.93.26'
#SERVER_PATH = '/json_post.php'
SERVER_PATH = '/upload'
#SERVER_PORT = 80
#SERVER_PORT = 443
#SERVER_PORT = 8080
HTTP_REQUEST_TIMEOUT = 5
RETRY_TIMEOUT = 3

def upload(waveseg_json):
	print 'uploading json...'
	try:
		headers = { 'content-type': 'application/json' }

		#conn = httplib.HTTPSConnection(SERVER_ADDRESS, SERVER_PORT, key_file='ssl-priv-snakeoil.key', cert_file='ssl-cert-snakeoil.key', timeout=HTTP_REQUEST_TIMEOUT)
		#conn = httplib.HTTPSConnection(SERVER_ADDRESS, SERVER_PORT, key_file='./asdf', cert_file='./asdf', timeout=HTTP_REQUEST_TIMEOUT)
		#conn = httplib.HTTPSConnection(SERVER_ADDRESS)

		conn = httplib.HTTPSConnection(SERVER_ADDRESS)
		#conn = httplib.HTTPConnection(SERVER_ADDRESS, SERVER_PORT)
		
		send_data = "Data= %s" % waveseg_json
		
		conn.request('POST', SERVER_PATH, send_data, headers)
		
		#print '----------------------------'
		#print waveseg_json
		#print send_data
		#print '---------------------------'
		
		response = conn.getresponse()
		print response.status, response.reason
		
		#print response.getheaders()
		#reply = response.read()
		#print reply

		conn.close()

	except Exception as detail:
		print 'Run-time Error in upload():', detail
		return False

	#response.status = 200 # for now...

	if response.status != 200:
		return False
	return True

class UploadThread(threading.Thread):

	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self):
		super(UploadThread, self).__init__()
		self._stop = threading.Event()
		self._data_ready = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()

	def data_ready(self):
		self._data_ready.set()

	def run(self):
		db = sqlite3.connect(DB_FILENAME)
		
		waveseg = WaveSeg()

		while True:
			if self._stop.isSet():
				break

			print('upload...')

			cur = db.cursor()
			cur.execute('SELECT * FROM WaveSeg WHERE UploadTime is NULL')
			cur.close()
			

			count = 0
			for db_tuple in cur:
				count += 1
				if self._stop.isSet():
					break
				cur_id = db_tuple[0]
				waveseg.init_from_db_tuple(db_tuple)
				waveseg_json = waveseg.get_json()

				if upload(waveseg_json):
					print 'upload success!'
					# update UploadTime field.
					cur1 = db.cursor()
					cur1.execute('UPDATE WaveSeg SET UploadTime = datetime() WHERE ID = ?', (cur_id,))
					db.commit()	
					cur1.close()
				else:
					print 'upload failed! retrying after %d seconds ...'%RETRY_TIMEOUT
					time.sleep(RETRY_TIMEOUT)
					break

			if count <= 0:
				print 'upload done wait ...'
				self._data_ready.clear()
				self._data_ready.wait()
		
		# clean up...
		db.close()

def clean_up():
	global upload_thread
	print
	print 'closing...'
	upload_thread.stop()
	upload_thread.data_ready()
	upload_thread.join()

def main():
	global upload_thread, DB_FILENAME

	print 'ANDROID upthread'

	# android has ANDROID_DATA key.
	if 'ANDROID_DATA' in os.environ:
	#if True:
		DB_FILENAME = '/sdcard/waveseg_db'
	else:
		DB_FILENAME = './waveseg_db'

	upload_thread = UploadThread()
	upload_thread.start()

	while True:
		upload_thread.data_ready()
		time.sleep(5)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		clean_up()

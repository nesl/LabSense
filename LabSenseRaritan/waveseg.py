import json

API_KEY = '-----BEGIN RSA PRIVATE KEY-----\
MIIEqQIBAAKCAQEArYowiHMdDo4A+CbY0KiFNLGhnM9deRMZJhcGZcCTmDHLktGb\
qKbssbvDiOu+FIjuIDo17s9QMvTuaaoERnc6ZH5iaH3CAVcjdbE75p665Fv8aJh+\
N8FQ3fjM2ed0JoueF+ktDApqzh4dzZSRwMoALWOYb9Zi6dq1cSuTN4eGdO05FiSx\
GEAdCEoPPCcDYMj+xGu3yubHSU69o5QdxJAstRGY2rRh3ruwNYyY5n50BkFZnxyg\
izgC0I65uIt9OgoYhRQ4ztsZw1fPDsm0GTbvdYKhvNpsQdh12xxhQeqLYwSP80JB\
Xj9ivWIj9aW3prd8MAhaJVyl0KaG9NibZmPawwIDAQABAoIBAQCVQrZbpibnzdun\
lEIHtepcWCvY48JR0Mtgp40pF2nbDXk63m4zsN8EP6r+qUTkBKJLtcWNkWI5cdFd\
sI3czc+7f7jEhuXGoVwubjJHOV8l6rg+fmqRKgST5trK0Phl7tAbYMMOCCe1ANJB\
b/etChD8+RyzlIGfAi3tGL2WlUpgZf3lfL5Wv56iXy9wJa6b3OpkVDq/bSwYP6UW\
Y/4HgYQfLvQ5zVQwwscMALAvO0rXUTMT54oRZS3Co1RjM8A+8JKQpQ5WZBdQI4Td\
K0AOrmUJ4ShCqncJvN7a0L7poo9EFvPZJCS+4mEVznC14OW6eKbJIyh6LkFsmlTV\
xUPbwjyBAoIAgQDGZPuvEHLRZ85rbuV3SLUnq3/ziL8hUf2yuaH8PP4gAAF0ipC0\
sJ1Kl7q9+Cg3tJjjlGZ7/s1vPXuTtE/4BoBNl86+q1UCUR1PJzQWumJYha+dn9wp\
lZMqQnfGNH0YzdX2litJh8WMbJmaRYlnO9XHVClUWmySWTUsRgbTxr5aJwKCAIEA\
3+22+oezw/OfPNaIsTgSEV6KZjZ+EVdBEX+9kuhvexUvcfPY6bgUHZxU0MIarU0+\
Uo7XbsWbe+w67+yBswp6hrBFQ4Pd9FRi85WwqKk/LDn8yfavqkZNr3noSRyJBR5Y\
kEewl515VCJ/aCtqmDtdqvff9b7q3TV7YCHgH7B6KAUCggCAW47dDDTWGEgE3lXG\
dl9Koy0llpmkQ1dYcrPyyrrHOLNn+IW+NHVRkcwmNWeh/9tLt7OT/GNiIZVJQ6gy\
Q6+UZLrLgfkF+VS/5vibtGV934aKvn65F0PdL+KO7hzpIppTxUIWZg/Pnne8B5NR\
zx+xEBWKIVC9zGh4/p6upeuRi38CggCAARjH+agqgD40PHcMilms9PrSkLeZnHoh\
7nUCt7J9wUuUROmd2V82cgKvA6q/uLOVJ5Bdi8RaA5xfmYc+B2N4wCoi3LbLooO7\
TFgiWmEh1xSdoVuc9qeLf92H/ruuDCFe663+Nm/mBTx6BUeZKQ+5YLoAFdMOkXDO\
nuTrlRwnLQUCggCBAJaW4bTa4UUyyezqZ7fhfIVO3MHiVqr1gcap0t45uWHkzpUN\
+CdGtKMFFViZNPUhmpmEWMJUzv8BROzcue9xpg4pWqk6iFy4zDW61kLCPTv1kX+L\
wSoF3MYpz5JmIqhDY2KrzHGoCsBy8DDTq13aCoNonsiA8fGkh4O1gVyt/BxZ\
-----END RSA PRIVATE KEY-----'

class WaveSeg:
	def __init__(self, wss_id = None, start_time = None, sampling_interval = None, static_location = None , value_blob = None):
		self.wss_id = wss_id
		self.start_time = start_time
		self.sampling_interval = sampling_interval
		self.static_location = static_location
		if value_blob != None:
			self.value_blob = value_blob
		else:
			self.value_blob = []

	def init_from_db_tuple(self, db_tuple):
		self.wss_id = db_tuple[2]
		self.start_time = db_tuple[3]
		self.sampling_interval = db_tuple[4]
		self.static_location = json.loads(db_tuple[5])
		self.value_blob = json.loads(db_tuple[6])

	def get_db_tuple(self):
		tuple = (None, None, self.wss_id, self.start_time, self.sampling_interval, json.dumps(self.static_location), json.dumps(self.value_blob))
		return tuple
    
	def get_json(self):
		waveseg_dict = {}
		waveseg_dict['WaveSegSeries'] = self.wss_id
		waveseg_dict['APIKey'] = API_KEY

		waveseg_dict['WaveSeg'] = []
		waveseg_dict['WaveSeg'].append({})
		waveseg_dict['WaveSeg'][0]['StartTime'] = self.start_time
		waveseg_dict['WaveSeg'][0]['SamplingInterval'] = self.sampling_interval
		waveseg_dict['WaveSeg'][0]['StaticLocation'] = self.static_location
		waveseg_dict['WaveSeg'][0]['ValueBlob'] = self.value_blob

		return json.dumps(waveseg_dict)


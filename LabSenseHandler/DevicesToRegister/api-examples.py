### Example python script for SensorAct VPDS APIs

import httplib, urllib

### Change this to your own VPDS Server info.

VPDS_SERVER_IP = '128.97.93.51'
VPDS_SERVER_PORT = '9000'



headers = { "Content-type": "application/json",
	          "Accept": "text/plain" }

conn = httplib.HTTPConnection(VPDS_SERVER_IP + ":" + VPDS_SERVER_PORT)



### 1. Registering a user. ###

#body = '{ "username": "yourname", "password": "yourpassword", "email": "youremail@ucla.edu" }'
#body = '{ "username": "jtsao322", "password": "neslrocks!", "email": "jtsao22@gmail.com" }';
#conn.request("POST", "/user/register", body, headers)



### 2. Login and getting API key. ###
#body = '{ "username": "jtsao322", "password": "neslrocks!" }'
#conn.request("POST", "/user/login", body, headers)


### 3. Change this to your own API key. ###

#API_KEY = 'Put your API key here'
API_KEY = '2bb5d6b943fc44f0bb6b467450e07ce7'



# 4. Adding a device.
"""
body = '{ "secretkey": "' + API_KEY + '", \
    "deviceprofile": { \
        "devicename": "NESL-PlugCom-1", \
        "location": "BH1762/UCLA", \
        "tags": "PlugCom", \
        "IP": "0.0.0.0", \
        "latitude": 0.0, \
        "longitude": 0.0, \
        "actuators": [ \
            { "name": "Thermostat", \
                "aid": "1" \
            } \
        ], \
        "sensors": [ \
            { "name": "Motion", \
                "sid": "1", \
                "channels": [ \
                    { "name": "MotionData", \
                        "type": "Boolean", \
                        "unit": "None", \
                        "samplingperiod": 1 \
                    } \
                ] \
            } \
        ] \
    } \
}'

conn.request("POST", "/device/add", body, headers)

"""

### 5. Upload sensor data. ###
body = '{ "secretkey": "' + API_KEY + '", \
	"data": { \
		"dname": "NESL-PlugCom-1", \
		"sname": "Motion", \
		"sid": "1", \
		"sinterval": "300", \
		"timestamp": 1351284531, \
		"loc": "BH1762/UCLA", \
		"channels": [ { \
			"cname": "MotionValue", \
			"unit": "None", \
			"readings": [ \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1, \
				0, 1, 0, 1, 0, 1, 0, 1, 0, 1 \
			] \
		} ] \
	} \
}'
conn.request("POST", "/data/upload/wavesegment", body, headers)


### 6. Querying data ###
"""
body = '{ "secretkey": "' + API_KEY + '", \
	"username": "haksoochoi", \
	"devicename": "NESL-PlugCom-1", \
	"sensorname": "Motion", \
	"sensorid": "1", \
	"channelname": "MotionData", \
	"conditions": { \
		"fromtime": 1351284531, \
		"totime": 1351284532 \
	} \
}'
conn.request("POST", "/data/query", body, headers)
"""



# List devices.
#body = '{ "secretkey": "' + API_KEY + '" }'
#conn.request("POST", "/device/list", body, headers)

# Delete device
#body = '{ "secretkey": "' + API_KEY + '", \
	#"devicename": "NESL-PlugCom-1" \
#}'

#conn.request("POST", "/device/delete", body, headers)



r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
print data1
conn.close()


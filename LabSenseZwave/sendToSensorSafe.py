#
#   SensorSafe Data Transmitter
#   Connects SUB socket to tcp://localhost:5556
#   Collects data from Zwave interface using Zeromq and
#      sends the data in JSON to SensorSafe
#

import sys
import zmq
import httplib, urllib
import json
import time
import datetime
from api_key import key
SERVER_ADDRESS = "128.97.93.29"
SERVER_PREFIX = ""
HTTP_REQUEST_TIMEOUT = 60
API_KEY = key

def sendToSensorSafe(json_data_to_upload):
    # Upload!
    try:
            params = urllib.urlencode({'apikey': API_KEY, 'data': json.dumps(json_data_to_upload)})
            conn = httplib.HTTPSConnection(SERVER_ADDRESS, timeout=HTTP_REQUEST_TIMEOUT)
            conn.request('POST', SERVER_PREFIX + '/upload/', params)
            response = conn.getresponse()

            print response.status, response.reason
            print response.getheaders()
            reply = response.read()
            print reply
            conn.close()
    except Exception as detail:
            print 'Error:', detail

def main():
    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print "Collecting data from Zwave..."
    socket.connect ("tcp://localhost:5556")

    # Subscribe to all zeromq messages
    # filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
    # socket.setsockopt(zmq.SUBSCRIBE, "Luminance")
    # socket.setsockopt(zmq.SUBSCRIBE, "Temperature")
    # socket.setsockopt(zmq.SUBSCRIBE, "Motion")
    socket.setsockopt(zmq.SUBSCRIBE, "")

    # Initialize variables
    temperature = None
    luminance = None
    motion = None
    door = 0    # Door is closed by default

    # Continually receive data from zwave and send data to SensorSafe
    while(1):
        string = socket.recv()
        string_list = string.split()
        measurement = string_list[0]
        str_value = string_list[1]
        # measurement, str_value, end_of_string = string.split()

        value = float(str_value)
        # print "%s: %f" % (measurement, float(value))

        if measurement == "Temperature":
            temperature =  value
        elif measurement == "Luminance":
            luminance = value
        elif measurement == "Motion":
            motion = value
        elif measurement == "Door":
            door = value

        if(temperature != None and luminance != None and motion != None):
            print "All variables are ready!"
            print "Temperature: ", temperature
            print "Luminance: ", luminance
            print "Motion: ", motion
            print "Door: ", door

            print "Sending to SensorSafe"
            sensorData = {
                "sampling_interval": 2,
                "timestamp": int(round(time.time()*1000)),
                "location": {"latitude": 34.068839550018311, "longitude": -118.44383955001831},
                "data_channel": [ "Temperature", "Luminance", "Motion", "Door"],
                "data": [[temperature, luminance, motion, door]]
            }
            sendToSensorSafe(sensorData)

            temperature = None
            luminance = None
            motion = None

if __name__ == "__main__":
    main()

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

    sendAll(socket)

def sendAll(socket):
    ''' This function waits for all variables to be available and continuously sends them as values come in '''
    # Initialize variables
    temperature = None
    luminance = None
    motion = 0
    motion_timeout = None   # This is the time the last motion was detected
                            # until it sends a Z-wave OFF command
    door = 0    # Door is closed by default
                # 0.0 means door is closed, 1.0 means door is open

    # Continually receive data from zwave and send data to SensorSafe
    while(1):
        string = socket.recv()
        string_list = string.split()
        measurement = string_list[0]
        str_value = string_list[1]

        value = float(str_value)

        # Set values based on measurement
        if measurement == "Temperature":
            temperature =  value
        elif measurement == "Luminance":
            luminance = value
        elif measurement == "Motion":
            motion = value
        elif measurement == "MotionTimeout":
            motion_timeout = value
        elif measurement == "Door":
            door = value

        # Send when variables are ready
        if(temperature != None and luminance != None and motion_timeout != None):
            print "All variables are ready!"
            print "Temperature: ", temperature
            print "Luminance: ", luminance
            print "Motion: ", motion
            print "Motion Timeout: ", motion_timeout
            print "Door: ", door

            print "Sending to SensorSafe"
            sensorData = {
                "sampling_interval": 1,   # Sampling interval does not matter since we are sending one dataset at a time
                "timestamp": int(round(time.time()*1000)),
                "location": {"latitude": 34.068839550018311, "longitude": -118.44383955001831},
                "data_channel": [ "Temperature", "Luminance", "Motion", "Motion Timeout", "Door"],
                "data": [[temperature, luminance, motion, motion_timeout, door]]
            }
            sendToSensorSafe(sensorData)

            # Reset values that will change
            # temperature = None
            # luminance = None
            # motion_timeout = None

if __name__ == "__main__":
    main()

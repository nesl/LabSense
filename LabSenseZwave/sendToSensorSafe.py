#
#   SensorSafe Data Transmitter
#   Connects SUB socket to tcp://localhost:5556
#   Collects data from Zwave interface using Zeromq and
#      sends the data in JSON to SensorSafe
#

import sys
import zmq

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


temperature = None
luminance = None
motion = None
door = 0    # Door is closed by default
# Continually receive data from zwave and send data to SensorSafe
while(1):
    string = socket.recv()
    measurement, str_value, end_of_string = string.split()

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

        temperature = None
        luminance = None
        motion = None
        door = None


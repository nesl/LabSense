"""
SensorSafe Data Transmitter
Connects socket to tcp://localhost:5556
Collects data from Zwave interface using Zeromq and
   sends the data in JSON to SensorSafe

Usage: python sendToSensorSafe.py [api-key] [Options]"

    [api-key] is the API key given when registering for a SensorSafe account.

    Options:

        -f [frequency]
            This is the number of seconds between each http request
            to SensorSafe."

            If [frequency] is not specified or is set to 0, the requests
                are made every time the data is received by the zeromq socket.

        -e This option specifies that all event-driven measurements should be
           sent right away (usually because they are more time-critical)
           instead of sending based on the frequency. Note that the none
           event-driven measurements will still be governed by the frequency
           and are not affected. Currently, the event-driven measurements
           are Motion and Door Status (Open/Closed).

        -v Verbose option that shows more information about the upload to
           SensorSafe.
"""

import sys              # Used for commandline arguments
import httplib          # Used for http requests
import urllib           # Used for http requests
import json             # Used for json formatted data
import time             # Used for timestamps
import threading        # Used for creating separate thread for sending to
                            # SensorSafe
import getopt           # Used for command line option handling
import zmq              # Used for receiving data sent over zeromq socket
import signal           # Used for properly cancelling timer thread when Ctrl-c
                            # is pressed

SERVER_ADDRESS = "128.97.93.29"
SERVER_PREFIX = ""
HTTP_REQUEST_TIMEOUT = 60

# Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
PURPLE = "\033[95m"
ENDCOLOR = "\033[0m"


class SensorVariableTracker:
    """ This class keeps track of all variables received from LabSenseZwave
        over the Zeromq socket and delivers the data to the
        SensorSafe server every [frequency] seconds. """

    def __init__(self, key, event_driven, verbose, frequency=0):
        """ Initialize the Zeromq socket to receive data
            and initialize timer thread to send data at given
            frequency. """

        #  Socket to talk to server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        self.socket.connect("tcp://localhost:5556")

        # Subscribe to all zeromq messages
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

        # This is the frequency at which the data will be sent to SensorSafe in
        # seconds
        self.frequency = frequency

        # sensorData keeps track of all the data entries that need to be sent
        # to SensorSafe
        self.sensorData = []

        # event_driven specifies if the event driven measurements should be
        # sent right away because they are more time
        # critical. Currently event driven measurements are Motion and Door.
        # Note: the none-event-driven variables are still controlled by the
        # frequency
        self.event_driven = event_driven

        # if verbose is true, more information about the upload process will be
        # printed
        self.verbose = verbose

        self.key = key

        # Start separate thread that runs sendSensorData every [frequency]
        # seconds
        if frequency > 0:
            print "Starting Timer with frequency " + str(frequency)
            self.timer_thread = threading.Timer(self.frequency,
                    self.sendSensorData)
            self.timer_thread.start()

            # Set up Ctrl-C signal handler
            def signal_handler(signal, frame):
                self.timer_thread.cancel()
                sys.exit(0)

            signal.signal(signal.SIGINT, signal_handler)

    def registerValue(self, measurement, value):
        """ Register a data entry to the sensorData list """

        if "Door" in measurement:
            color = BLUE
        elif "Energy" in measurement or "Power" in measurement:
            color = GREEN
        else:
            color = PURPLE
        cur_time = int(round(time.time() * 1000))

        print "%sRegistering %s: %s at %d %s" % (color, measurement, value,
                cur_time, ENDCOLOR)

        data_entry = {
                "sampling_interval": 1,
                "timestamp": cur_time,
                "location": {"latitude": 34.068839550018311,
                             "longitude": -118.44383955001831},
                "data_channel": [measurement],
                "data": [[value]]
        }
        # If option for sending event driven measurements is specified, send
        # the data immediately
        if self.event_driven == True and measurement in ("Motion", "Door"):
            success = self.sendToSensorSafe(data_entry)
            if not success:
                self.sensorData.append(data_entry)
        else:
            self.sensorData.append(data_entry)

        # When Frequency is 0, this is a special mode where values are sent at
        # the rate they are received
        if self.frequency == 0:
            self.sendSensorData()

    def receiveFromSocket(self):
        """ Continually receive data from zwave and send data to SensorSafe """

        print "Collecting data from Zwave..."
        while(1):
            string = self.socket.recv()

            string_list = string.split()
            measurement = string_list[0]
            str_value = string_list[1]

            self.registerValue(measurement, float(str_value))

    def sendSensorData(self):
        """ Send all sensor data to SensorSafe """

        for data_entry in self.sensorData:
            success = self.sendToSensorSafe(data_entry)
            # If data was sent successfully, delete the data from list. If not,
            # don't do anything.
            if success:
                self.sensorData.remove(data_entry)

        # Set a thread to keep calling this function if frequency was specified
        if self.frequency > 0:
            self.timer_thread = threading.Timer(self.frequency,
                                                self.sendSensorData)
            self.timer_thread.start()

    def sendToSensorSafe(self, json_data_to_upload):
        """ Send single data entry to SensorSafe """
        try:
            params = urllib.urlencode({'apikey': self.key,
                                      'data': json.dumps(json_data_to_upload)})
            conn = httplib.HTTPSConnection(SERVER_ADDRESS,
                                            timeout=HTTP_REQUEST_TIMEOUT)
            conn.request('POST', SERVER_PREFIX + '/upload/', params)
            response = conn.getresponse()

            if self.verbose == True:
                print response.status, response.reason
                print response.getheaders()
            reply = response.read()
            print reply
            conn.close()
            return True
        except IOError, detail:
            print ('No internet connection, will send the data when the'
                  ' internet becomes available')
            return False


def usage():
    """ Prints out the usage for the script """

    print """
Usage: python sendToSensorSafe.py [api-key] [Options]"

    [api-key] is the API key given when registering for a SensorSafe account.

    Options:

        -f [frequency]
            This is the number of seconds between each http request
            to SensorSafe."

            If [frequency] is not specified or is set to 0, the requests
                are made every time the data is received by the zeromq socket.

        -e This option specifies that all event-driven measurements should be
           sent right away (usually because they are more time-critical)
           instead of sending based on the frequency. Note that the none
           event-driven measurements will still be governed by the frequency
           and are not affected. Currently, the event-driven measurements are
           Motion and Door Status (Open/Closed).

        -v Verbose option that shows more information about the upload to
           SensorSafe.
       """

if __name__ == "__main__":
    # Check if number of arguments is adequate
    if len(sys.argv) < 2:
        print "Not enough arguments"
        usage()
        sys.exit(2)

    # Get the api key
    key = sys.argv[1]
    if len(key) != 40:
        print "Invalid key (Should be 40 characters long)"
        usage()
        sys.exit(2)
    frequency = 0

    # Parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[2:], "hevf:", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    event_driven = False
    verbose = False

    for option, argument in opts:
        if option == "-f":
            frequency = argument
        elif option == "-e":
            event_driven = True
        elif option == "-v":
            verbose = True
        elif option in ("-h", "--help"):
            usage()

    if frequency < 0:
        print "The frequency must be zero or greater."
        sys.exit(2)

    # Track the variables and send to SensorSafe
    svt = SensorVariableTracker(key, event_driven, verbose, int(frequency))
    svt.receiveFromSocket()

import argparse                             # For parsing command line arguments
import SocketServer                         # For the socket server
import json                                 # For parsing json into python dictionary
import sys                                  # For importing from project directory
import os                                   # For importing from project directory
import Queue                                # For sink queues

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device
import LabSenseModbus.common.DataSinks.DataSink as DataSink
import LabSenseHandler.configReader as configReader

class LabSenseTCPHandler(SocketServer.BaseRequestHandler):
    """ The tcp handler for LabSense that adds the data
    coming to each of its queues."""

    def handle(self):
        """ Handle the TCP Handler traffic """

        try:
            # Receive the data
            data = self.request.recv(1024)
        except socket.error:
            print "Connection reset by peer..."
            return

        json_data = json.loads(data)
        #print "Json data: ", json_data
        
        # Verify Api Key
        if json_data["API_KEY"] == self.server.api_key:
            # Convert the unicode json to string json
            converted_data = configReader.convert(json_data["data"])
            self.notify(converted_data["devicename"],
                        converted_data)
        else:
            print "Received message from unverified Api key."

    def notify(self, device, data):
        if data:
            for queue in self.server.queues[device]:
                queue.put(data)

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("Port", help="Port to serve tcp handler on.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    name = "LabSenseServer"

    # Initialize the LabSenseServer
    HOST = ""
    server = SocketServer.TCPServer((HOST, int(args.Port)), LabSenseTCPHandler)
    server.queues = {}

    # Initialize tcp handler with api key
    server.api_key = config[name]["API_KEY"]

    # LabSenseServer has several sensors
    for innerNode, innerConfig in config[name]["Sensors"].iteritems():
        """ Attaches sinks to devices based on configuration file. """
        first_time = True
        for sink in ["SensorAct", "Cosm", "Stdout"]:
            if innerConfig[sink]:
                interval = innerConfig[sink + "Interval"]
                queue = Queue.Queue()

                if first_time:
                    server.queues[innerConfig["name"]] = []
                    first_time = False

                # server.queues is a dictionary with:
                # keys: name of Device
                # values: list of queues for that device
                server.queues[innerConfig["name"]].append(queue)
                dataSink = DataSink.DataSink.dataSinkFactory(sink, config, queue, interval)
                dataSink.registerDevice(innerConfig["name"])
                threads.append(dataSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()

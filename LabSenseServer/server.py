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

        # Receive the data
        data = self.request.recv(1024)
        print "Data: ", data
        json_data = json.loads(data)
        print "Json data: ", json_data
        self.notify(json_data)

    def notify(self, data):
        if data:
            for queue in self.server.queues:
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
    server.queues = []

    # LabSenseServer has several sensors
    for innerNode, innerConfig in config[name].iteritems():
        """ Attaches sinks to devices based on configuration file. """
        for sink in ["SensorAct", "Cosm", "Stdout"]:
            if innerConfig[sink]:
                interval = innerConfig[sink + "Interval"]
                queue = Queue.Queue()
                server.queues.append(queue)
                dataSink = DataSink.DataSink.dataSinkFactory(sink, config, queue, interval)
                threads.append(dataSink)

    #if config[name]["SensorAct"]:
        #sensorActInterval = config[name]["SensorActInterval"]
        #sensorActQueue = Queue.Queue();
        #sensorActSink = SensorActSink(config,
                #sensorActQueue, sensorActInterval)
        #server.queues.append(sensorActQueue)
        #threads.append(sensorActSink)

    #if config[name]["Cosm"]:
        #cosmInterval = config[name]["CosmInterval"]
        #cosmQueue = Queue.Queue()
        #cosmSink = CosmSink(config, cosmQueue, cosmInterval)
        #server.queues.append(cosmQueue)
        #threads.append(cosmSink)

    #if config[name]["Stdout"]:
        #stdoutInterval = config[name]["StdoutInterval"]
        #stdoutQueue = Queue.Queue()
        #stdoutSink = StdoutSink(config, stdoutQueue,
                #stdoutInterval)
        #server.queues.append(stdoutQueue)
        #threads.append(stdoutSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()

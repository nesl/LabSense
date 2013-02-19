import argparse                             # For parsing command line arguments
import SocketServer                         # For the socket server
import json                                 # For parsing json into python dictionary
import sys                              # for importing from project directory
import os                               # for importing from project directory

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device
import LabSenseHandler.configReader as configReader

class LabSenseTCPHandler(SocketServer.BaseRequestHandler, Device):
    """ The tcp handler for LabSense that adds the data
    coming to each of its queues."""

    def handle(self):
        """ Handle the TCP Handler traffic """

        # Receive the data
        data = self.request.recv(1024)
        print "Data: ", data
        json_data = json.loads(data)
        print "Json data: ", json_data

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("Port", help="Port to serve tcp handler on.")
    args = parser.parse_args()

    HOST = ""
    server = SocketServer.TCPServer((HOST, int(args.Port)), LabSenseTCPHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()

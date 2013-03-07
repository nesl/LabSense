import argparse                             # For parsing command line arguments
import SocketServer                         # For the socket server
import json                                 # For parsing json into python dictionary
import sys                                  # For importing from project directory
import os                                   # For importing from project directory
import Queue                                # For sink queues

sys.path.insert(1, os.path.abspath("../.."))
from Devices.Device import Device

class LabSenseServer(SocketServer.TCPServer):
    """ This class handles traffic coming into LabSenseServer """

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
                try:
                    # Put the data in the queues according to the device
                    for queue in self.server.queues[device]:
                        queue.put(data)
                except KeyError:
                    # If no queue was made for the device, let it pass
                    pass

    def __init__(self, host, port, api_key):
        self.api_key = api_key
        # server.queues is a dictionary with:
        #   keys: name of Device
        #   values: list of queues for that device
        self.queues = {}
        self.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self, (host, port), self.LabSenseTCPHandler)

if __name__ == "__main__":

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink

    # Parse command line for arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration path.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.readConfiguration(args.config)

    # Create communication threads
    threads = []

    # Get the device config
    server_name = "LabSenseServer"
    server_config = config[server_name]

    # Initialize the LabSenseServer
    HOST = ""
    server = LabSenseServer(HOST, int(server_config["PORT"]), server_config["API_KEY"])

    # LabSenseServer has several sensors: DoorSensor and MotionSensor
    for device, device_config in server_config["Sensors"].iteritems():
        """ Attaches sinks to devices based on configuration file. """
        first_time = True
        for sink in ["SensorAct", "Cosm", "Stdout"]:
            if device_config[sink]:
                interval = device_config[sink + "Interval"]
                queue = Queue.Queue()
                device_name = device_config["name"]

                if first_time:
                    server.queues[device_name] = []
                    first_time = False

                server.queues[device_name].append(queue)
                dataSink = DataSink.dataSinkFactory(sink, config[sink], queue, interval)
                dataSink.registerDevice(device, device_config)
                threads.append(dataSink)

    # Start threads
    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    # Keep running the server forever
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)


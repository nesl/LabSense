import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../.."))
from RaritanClient import RaritanClient 
from Devices.Device import Device 

import LabSenseHandler.configReader as configReader

class RaritanDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval, username, password):
        super(RaritanDevice, self).__init__(sinterval)
        self.channels = channels
        self.client = RaritanClient(name, IP, PORT, channels, username, password)

if __name__ == "__main__":

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration of Raritan Device.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.readConfiguration(args.config)

    # Create communication threads
    threads = []

    # Get the device config
    device_name = "Raritan"
    device_config = config[device_name]

    # Initialize the Raritan Device thread
    device = RaritanDevice(device_config["name"],
                           device_config["IP"],
                           device_config["PORT"],
                           device_config["channels"], 
                           device_config["sinterval"],
                           device_config["username"],
                           device_config["password"])
    threads.append(device)

    # Attach the sinks
    for sink in ["SensorAct", "Cosm", "Stdout"]:
        if device_config[sink]:
            interval = device_config[sink + "Interval"]
            queue = Queue.Queue()
            device.attach(queue)
            dataSink = DataSink.dataSinkFactory(sink, config[sink], queue, interval)
            dataSink.registerDevice(device_name, device_config)
            threads.append(dataSink)

    print "Number of threads: ", len(threads)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

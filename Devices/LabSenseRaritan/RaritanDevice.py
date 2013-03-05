import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../.."))
from RaritanClient import RaritanClient 
from Devices.Device import Device 

import LabSenseHandler.configReader as configReader

class RaritanDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(RaritanDevice, self).__init__(sinterval)
        self.channels = channels
        self.client = RaritanClient(name, IP, PORT, channels)

if __name__ == "__main__":

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Raritan device")
    parser.add_argument("IP", help="IP address for Raritan")
    parser.add_argument("PORT", help="Port for Raritan")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Raritan.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    device_name = "Raritan"

    # Initialize the Raritan Device thread
    device = RaritanDevice(args.name, args.IP, args.PORT,
            config[device_name]["channels"], config[device_name]["sinterval"])
    threads.append(device)

    # Attach the sinks
    device_config = config[device_name]
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

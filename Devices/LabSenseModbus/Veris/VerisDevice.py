import argparse                             # For parsing command line arguments
import sys                                  # For importing from common directory
import os                                   # For importing from common directory
import time                                 # For sampling time
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../../.."))
from VerisClient import VerisClient
from Devices.Device import Device

class VerisDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(VerisDevice, self).__init__(sinterval)
        self.name = name
        self.channels = channels
        self.devicename = "Veris"
        self.client = VerisClient(name, IP, PORT, channels)

if __name__ == "__main__":
    # import config and DataSink
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink

    # Parse command line for arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Veris device")
    parser.add_argument("IP", help="IP address for Veris")
    parser.add_argument("PORT", help="Port for Veris")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Veris.")
    args = parser.parse_args()

    device_name = "Veris"

    # Read configuration
    config = configReader.config
    device_config = config[device_name]

    # Create communication threads
    threads = []


    # Initialize the Veris Device
    device = VerisDevice(args.name, args.IP, args.PORT,
            config[device_name]["channels"], config[device_name]["sinterval"])
    threads.append(device)

    # Attach sinks
    for sink in ["SensorAct", "Cosm", "Stdout"]:
        if device_config[sink]:
            interval = device_config[sink + "Interval"]
            queue = Queue.Queue()
            device.attach(queue)
            dataSink = DataSink.dataSinkFactory(sink, config[sink], queue, interval)
            dataSink.registerDevice(device_name, device_config)
            threads.append(dataSink)

    # Start threads
    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

import argparse                             # For parsing command line arguments
import sys                                  # For importing from common directory
import os                                   # For importing from common directory
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../../.."))
from VerisClient import VerisClient
from Devices.Device import Device

class VerisDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(VerisDevice, self).__init__(sinterval)
        self.client = VerisClient(name, IP, PORT, channels)

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
    device_name = "Veris"
    device_config = config[device_name]

    # Initialize the Veris Device
    device = VerisDevice(device_config["name"],
                         device_config["IP"],
                         device_config["PORT"],
                         device_config["channels"], 
                         device_config["sinterval"])
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

    # Keep on running forever
    for thread in threads:
        while thread.isAlive():
            thread.join(5)

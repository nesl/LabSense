import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads

from EatonClient import EatonClient
from common.Device import Device
from common.DataSinks.StdoutSink import StdoutSink
from common.DataSinks.SensorActSink import SensorActSink
from common.DataSinks.CosmSink import CosmSink 


sys.path.insert(0, os.path.abspath("../.."))
import LabSenseHandler.configReader as configReader

""" Represents a Eaton device. """
class EatonDevice(Device):

    def __init__(self, name, IP, PORT, channels):
        super(EatonDevice, self).__init__()
        self.name = name
        self.channels = channels
        self.devicename = "Eaton"
        self.client = EatonClient(name, IP, PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Eaton device")
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Eaton.")
    args = parser.parse_args()

    config = configReader.config
    # Initialize the Eaton Device
    device = EatonDevice(args.name, args.IP, args.PORT,
            config["Eaton"]["channels"])

    # Create DataSinks
    stdoutSink = StdoutSink()
    sensorActSink = SensorActSink(config)
    cosmSink = CosmSink(config)

    # Attach DatSinks
    device.attach(stdoutSink)
    device.attach(sensorActSink)
    device.attach(cosmSink)

    sample_time = float(args.time)
    while True:
        data = device.getData()
        time.sleep(sample_time)

import argparse                             # For parsing command line arguments
import sys                                  # For importing from common directory
import os                                   # For importing from common directory
import time                                 # For sampling time

from VerisClient import VerisClient

# Import from common directory
sys.path.insert(0, os.path.abspath("../.."))

import LabSenseHandler.configReader as configReader

from common.Device import Device
from common.DataSinks.StdoutSink import StdoutSink
from common.DataSinks.SensorActSink import SensorActSink
from common.DataSinks.CosmSink import CosmSink 

class VerisDevice(Device):

    def __init__(self, name, IP, PORT, channels):
        super(VerisDevice, self).__init__()
        self.name = name
        self.devicename = "Veris"
        self.channels = channels
        self.client = VerisClient(name, IP, PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Veris device")
    parser.add_argument("IP", help="IP address for Veris")
    parser.add_argument("PORT", help="Port for Veris")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Veris.")
    args = parser.parse_args()

    config = configReader.config
    # Initialize the Veris Device
    device = VerisDevice(args.name, args.IP, args.PORT,
            config["Veris"]["channels"])

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

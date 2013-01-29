import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads

from RaritanClient import RaritanClient 

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbusPy.common.Device import Device 
from LabSenseModbusPy.common.Device import Device
from LabSenseModbusPy.common.DataSinks.StdoutSink import StdoutSink
from LabSenseModbusPy.common.DataSinks.SensorActSink import SensorActSink
from LabSenseModbusPy.common.DataSinks.CosmSink import CosmSink 

import LabSenseHandler.configReader as configReader

class RaritanDevice(Device):

    def __init__(self, name, IP, PORT, channels):
        super(RaritanDevice, self).__init__()
        self.name = name
        self.channels = channels
        self.devicename = "Raritan"
        self.client = RaritanClient(name, IP, PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Raritan device")
    parser.add_argument("IP", help="IP address for Raritan")
    parser.add_argument("PORT", help="Port for Raritan")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Raritan.")
    args = parser.parse_args()

    config = configReader.config
    # Initialize the Raritan Device
    device = RaritanDevice(args.name, args.IP, args.PORT,
            config["Raritan"]["channels"])

    # Create DataSinks
    #stdoutSink = StdoutSink()
    sensorActSink = SensorActSink(config)
    cosmSink = CosmSink(config)

    # Attach DatSinks
    #device.attach(stdoutSink)
    device.attach(sensorActSink)
    device.attach(cosmSink)

    sample_time = float(args.time)
    while True:
        data = device.getData()
        time.sleep(sample_time)

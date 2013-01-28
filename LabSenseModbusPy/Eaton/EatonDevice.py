import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
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
        self.devicename = "Eaton"
        self.name = name
        self.channels = channels
        super(EatonDevice, self).__init__(name)
        self.eatonClient = EatonClient(name, IP, PORT)

    def getData(self):
        data = self.eatonClient.getData(self.channels)
        self.notify(data)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Eaton device")
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    device = EatonDevice(args.name, args.IP, args.PORT,
            configReader.config["Eaton"]["channels"])

    stdoutSink = StdoutSink()
    sensorActSink = SensorActSink()
    cosmSink = CosmSink()

    device.attach(stdoutSink)
    device.attach(sensorActSink)
    device.attach(cosmSink)
    data = device.getData()

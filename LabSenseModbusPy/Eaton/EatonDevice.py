import argparse                             # For parsing command line arguments

from EatonClient import EatonClient
from common.Device import Device
from common.DataSinks.StdoutSink import StdoutSink
from common.DataSinks.SensorActSink import SensorActSink

""" Represents a Eaton device. """
class EatonDevice(Device):

    def __init__(self, name, IP, PORT, fields):
        super(EatonDevice, self).__init__()
        self.eatonClient = EatonClient(name, IP, PORT, fields)

    def getData(self):
        data = self.eatonClient.getData()
        self.notify(data)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Eaton device")
    parser.add_argument("IP", help="IP address for Eaton")
    parser.add_argument("PORT", help="Port for Eaton")
    args = parser.parse_args()

    fields_to_read = ["CurrentA", "CurrentB", "CurrentC"]
    device = EatonDevice(args.name, args.IP, args.PORT, fields_to_read)

    stdoutSink = StdoutSink()
    sensorActSink = SensorActSink()
    device.attach(stdoutSink)
    device.attach(sensorActSink)
    data = device.getData()

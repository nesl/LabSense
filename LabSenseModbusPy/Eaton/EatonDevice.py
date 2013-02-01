import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from EatonClient import EatonClient
from common.Device import Device
from common.DataSinks.StdoutSink import StdoutSink
from common.DataSinks.SensorActSink import SensorActSink
from common.DataSinks.CosmSink import CosmSink 


sys.path.insert(0, os.path.abspath("../.."))
import LabSenseHandler.configReader as configReader

""" Represents an Eaton device. """
class EatonDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(EatonDevice, self).__init__(sinterval)
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

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    name = "Eaton"

    # Initialize the Eaton Device
    device = EatonDevice(args.name, args.IP, args.PORT,
            config[name]["channels"], config[name]["sinterval"])
    threads.append(device)

    if config[name]["SensorAct"]:
        sensorActQueue = Queue.Queue()
        sensorActSink = SensorActSink(config, sensorActQueue)
        device.attach(sensorActQueue)
        threads.append(sensorActSink)

    if config[name]["Cosm"]:
        cosmQueue = Queue.Queue()
        cosmSink = CosmSink(config, cosmQueue)
        device.attach(cosmQueue)
        threads.append(cosmSink)

    if config[name]["Stdout"]:
        stdoutQueue = Queue.Queue()
        stdoutSink = StdoutSink(config, stdoutQueue)
        device.attach(stdoutQueue)
        threads.append(stdoutSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

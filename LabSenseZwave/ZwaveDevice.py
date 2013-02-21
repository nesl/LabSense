import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from ZwaveClient import ZwaveClient 

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device 
from LabSenseModbus.common.Device import Device
from LabSenseModbus.common.DataSinks.StdoutSink import StdoutSink
from LabSenseModbus.common.DataSinks.SensorActSink import SensorActSink
from LabSenseModbus.common.DataSinks.CosmSink import CosmSink 

import LabSenseHandler.configReader as configReader

class ZwaveDevice(Device):

    def __init__(self, IP, PORT, channels, sinterval):
        super(ZwaveDevice, self).__init__(sinterval)
        self.client = ZwaveClient(IP, PORT, channels)

    """ Device Overwritten functions """

    def getData(self):
        """ getData overrides Device's getData because querying the Vera returns
        data for several zwave devices """
        data = self.client.getData()
        for datum in data:
            self.notify(datum)
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("IP", help="IP address for SmartSwitch")
    parser.add_argument("PORT", help="Port for SmartSwitch")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from SmartSwitch.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []

    # Initialize the SmartSwitch Device thread
    device = ZwaveDevice(args.IP, args.PORT,
            [], 0) 
    threads.append(device)

    Zwave_config = config["Zwave"]

    if zwave_config[name]["SensorAct"]:
        sensorActInterval = zwave_config[name]["SensorActInterval"]
        sensorActQueue = Queue.Queue();
        sensorActSink = SensorActSink(zwave_config,
                sensorActQueue, sensorActInterval)
        device.attach(sensorActQueue)
        threads.append(sensorActSink)

    if zwave_config[name]["Cosm"]:
        cosmInterval = zwave_config[name]["CosmInterval"]
        cosmQueue = Queue.Queue()
        cosmSink = CosmSink(zwave_config, cosmQueue, cosmInterval)
        device.attach(cosmQueue)
        threads.append(cosmSink)

    if zwave_config[name]["Stdout"]:
        stdoutInterval = zwave_config[name]["StdoutInterval"]
        stdoutQueue = Queue.Queue()
        stdoutSink = StdoutSink(zwave_config, stdoutQueue,
                stdoutInterval)
        device.attach(stdoutQueue)
        threads.append(stdoutSink)

    print "Number of threads: ", len(threads)

    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from SmartSwitchClient import SmartSwitchClient
from LightSensorClient import LightSensorClient
from TemperatureSensorClient import TemperatureSensorClient

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device 
from LabSenseModbus.common.Device import Device
from LabSenseModbus.common.DataSinks.StdoutSink import StdoutSink
from LabSenseModbus.common.DataSinks.SensorActSink import SensorActSink
from LabSenseModbus.common.DataSinks.CosmSink import CosmSink 

import LabSenseHandler.configReader as configReader

class ZwaveDevice(Device):

    def __init__(self, devicename, name, IP, PORT, channels, sinterval):
        super(ZwaveDevice, self).__init__(sinterval)

        if devicename == "SmartSwitch":
            self.client = SmartSwitchClient(name, IP, PORT, channels)
        elif devicename == "LightSensor":
            self.client = LightSensorClient(name, IP, PORT, channels)
        elif devicename == "TemperatureSensor":
            self.client = TemperatureSensorClient(name, IP, PORT, channels)
        else:
            raise TypeError(devicename + " device unrecoganized.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("Name", help="Name for Zwave Device")
    parser.add_argument("Devicename", help="Device Name for Zwave Device.")
    parser.add_argument("IP", help="IP address for Zwave Device")
    parser.add_argument("PORT", help="Port for Zwave Device")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Zwave Device.")
    args = parser.parse_args()

    # Read configuration
    config = configReader.config

    # Create communication threads
    threads = []
    devicename = args.Devicename

    # Initialize the SmartSwitch Device thread
    device = ZwaveDevice(args.Name, devicename, args.IP, args.PORT,
            config[devicename]["channels"], config[devicename]["sinterval"])
    threads.append(device)

    if config[devicename]["SensorAct"]:
        sensorActInterval = config[devicename]["SensorActInterval"]
        sensorActQueue = Queue.Queue();
        sensorActSink = SensorActSink(config,
                sensorActQueue, sensorActInterval)
        device.attach(sensorActQueue)
        threads.append(sensorActSink)

    if config[devicename]["Cosm"]:
        cosmInterval = config[devicename]["CosmInterval"]
        cosmQueue = Queue.Queue()
        cosmSink = CosmSink(config, cosmQueue, cosmInterval)
        device.attach(cosmQueue)
        threads.append(cosmSink)

    if config[devicename]["Stdout"]:
        stdoutInterval = config[devicename]["StdoutInterval"]
        stdoutQueue = Queue.Queue()
        stdoutSink = StdoutSink(config, stdoutQueue,
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

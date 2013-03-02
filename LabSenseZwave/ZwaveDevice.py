import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from SmartSwitchClient import SmartSwitchClient
from LightSensorClient import LightSensorClient
from TemperatureSensorClient import TemperatureSensorClient

sys.path.insert(0, os.path.abspath(".."))
from LabSenseModbus.common.Device import Device 


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
    # Import configReader and DataSink
    import LabSenseHandler.configReader as configReader
    from LabSenseModbus.common.DataSinks.DataSink import DataSink

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
    device = ZwaveDevice(devicename, args.Name, args.IP, args.PORT,
            config[devicename]["channels"], config[devicename]["sinterval"])
    threads.append(device)

    device_config = config[devicename]
    for sink in ["SensorAct", "Cosm", "Stdout"]:
        if device_config[sink]:
            interval = device_config[sink + "Interval"]
            queue = Queue.Queue()
            device.attach(queue)
            dataSink = DataSink.dataSinkFactory(sink, config, queue, interval)
            dataSink.registerDevice(args.Name)
            threads.append(dataSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

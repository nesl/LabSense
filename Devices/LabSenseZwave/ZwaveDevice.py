import argparse                             # For parsing command line arguments
import sys, os                              # for importing from project directory
import time                                 # For sleeping between uploads
import Queue                                # For communicating between datasinks and devices

from SmartSwitchClient import SmartSwitchClient
from LightSensorClient import LightSensorClient
from TemperatureSensorClient import TemperatureSensorClient

device_path = os.path.join(os.path.dirname(sys.argv[0]), "../../")
sys.path.insert(1, device_path)
from Devices.Device import Device 

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

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration path.")
    parser.add_argument("Devicename", help="Choose between the following Zwave\
                        Devices: SmartSwitch, LightSensor, TemperatureSensor")
    parser.add_argument("name", help="Name of device (name field in config.json file)")
    args = parser.parse_args()

    # Read configuration
    config = configReader.readConfiguration(args.config)

    # Create communication threads
    threads = []

    # Get the device config
    device_name = args.Devicename
    for device, dev_config in config.iteritems():
        if device == device_name:
            if dev_config["name"] == args.name:
                device_config = dev_config

    # If the device is present, run it
    if device_config:
        print "Found %s device" % device_name

        # Initialize the Zwave Device thread
        device = ZwaveDevice(args.Devicename,
                             device_config["name"],
                             device_config["IP"],
                             device_config["PORT"],
                             device_config["channels"], 
                             device_config["sinterval"])
        threads.append(device)

        # Attach the sinks
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

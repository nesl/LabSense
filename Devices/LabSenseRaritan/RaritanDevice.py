import argparse                             # For parsing command line arguments
import sys                                  # For importing from common directory
import os                                   # For importing from common directory
import Queue                                # For communicating between datasinks and devices

device_path = os.path.join(os.path.dirname(sys.argv[0]), "../..")
sys.path.insert(1, device_path)
from RaritanClient import RaritanClient 
from Devices.Device import Device 

class RaritanDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval, username, password):
        super(RaritanDevice, self).__init__(sinterval)
        self.client = RaritanClient(name, IP, PORT, channels, username, password)

if __name__ == "__main__":

    # Import sinks and configReader
    import LabSenseHandler.configReader as configReader
    from DataSinks.DataSink import DataSink

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration path.")
    parser.add_argument("name", help="Name of device (name field in config.json file)")
    args = parser.parse_args()

    # Read configuration
    config = configReader.readConfiguration(args.config)

    # Create communication threads
    threads = []

    # Get the device config
    device_name = "Raritan"
    for device, dev_configs in config.iteritems():
        if (type(dev_configs)!=list):
            dev_configs = [dev_configs]
        for dev_config in dev_configs:
            if device == device_name:
                if dev_config["name"] == args.name:
                    device_config = dev_config

    # If the device is present, run it
    if device_config:
        print "Found %s device" % device_name
        # Initialize the Raritan Device thread
        device = RaritanDevice(device_config["name"],
                               device_config["IP"],
                               device_config["PORT"],
                               device_config["channels"], 
                               device_config["sinterval"],
                               device_config["username"],
                               device_config["password"])
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

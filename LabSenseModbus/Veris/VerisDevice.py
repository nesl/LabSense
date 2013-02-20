import argparse                             # For parsing command line arguments
import sys                                  # For importing from common directory
import os                                   # For importing from common directory
import time                                 # For sampling time
import Queue                                # For communicating between datasinks and devices

sys.path.insert(1, os.path.abspath("../.."))
from VerisClient import VerisClient
from LabSenseModbus.common.Device import Device

class VerisDevice(Device):

    def __init__(self, name, IP, PORT, channels, sinterval):
        super(VerisDevice, self).__init__(sinterval)
        self.name = name
        self.channels = channels
        self.devicename = "Veris"
        self.client = VerisClient(name, IP, PORT, channels)

if __name__ == "__main__":
    # import config and DataSink
    import LabSenseHandler.configReader as configReader
    from LabSenseModbus.common.DataSinks.DataSink import DataSink

    #from LabSenseModbus.common.DataSinks.StdoutSink import StdoutSink
    #from LabSenseModbus.common.DataSinks.SensorActSink import SensorActSink
    #from LabSenseModbus.common.DataSinks.CosmSink import CosmSink 

    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of Veris device")
    parser.add_argument("IP", help="IP address for Veris")
    parser.add_argument("PORT", help="Port for Veris")
    parser.add_argument("time", help="Time (in seconds) between each retrieval of data from Veris.")
    args = parser.parse_args()

    name = "Veris"

    # Read configuration
    config = configReader.config
    device_config = config[name]

    # Create communication threads
    threads = []


    # Initialize the Veris Device
    device = VerisDevice(args.name, args.IP, args.PORT,
            config[name]["channels"], config[name]["sinterval"])
    threads.append(device)

    #if config[name]["SensorAct"]:
        #sensorActInterval = config[name]["SensorActInterval"]
        #sensorActQueue = Queue.Queue();
        #sensorActSink = SensorActSink(config,
                #sensorActQueue, sensorActInterval)
        #device.attach(sensorActQueue)
        #threads.append(sensorActSink)

    #if config[name]["Cosm"]:
        #cosmInterval = config[name]["CosmInterval"]
        #cosmQueue = Queue.Queue()
        #cosmSink = CosmSink(config, cosmQueue, cosmInterval)
        #device.attach(cosmQueue)
        #threads.append(cosmSink)

    #if config[name]["Stdout"]:
        #stdoutInterval = config[name]["StdoutInterval"]
        #stdoutQueue = Queue.Queue()
        #stdoutSink = StdoutSink(config, stdoutQueue,
                #stdoutInterval)
        #device.attach(stdoutQueue)
        #threads.append(stdoutSink)

    for sink in ["SensorAct", "Cosm", "Stdout"]:
        if device_config[sink]:
            interval = device_config[sink + "Interval"]
            queue = Queue.Queue()
            device.attach(queue)
            dataSink = DataSink.dataSinkFactory(sink, config, queue, interval)
            threads.append(dataSink)

    print "Number of threads: ", len(threads)
    for thread in threads:
        thread.daemon = True
        thread.start()

    for thread in threads:
        while thread.isAlive():
            thread.join(5)

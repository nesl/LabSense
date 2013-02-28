import argparse                             # For parsing command line arguments
import sys                                  # For importing from project directory
import os                                   # For importing from project directory
import Queue                                # For communicating between datasinks and devices

import configReader                         # For reading the configuration

sys.path.insert(1, os.path.abspath(".."))
import LabSenseModbus.common.DataSinks.DataSink as DataSink
import LabSenseModbus.common.Device as Device

class LabSenseMain(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.threads = []

    def run(self):
        """ Parse nodes in Configuration file """
        for node, config in self.configuration.iteritems():
            # Sinks
            if node == "SensorAct":
                pass
            elif node == "Cosm":
                pass
            elif node == "Stdout":
                pass

            # Devices 
            elif node in ["Eaton", "Veris", "Raritan", "SmartSwitch",
                          "LightSensor", "TemperatureSensor"]:
                device = Device.Device.deviceFactory(node, 
                                                     config["name"], 
                                                     config["IP"], 
                                                     config["PORT"], 
                                                     config["channels"], 
                                                     config["sinterval"])
                self.threads.append(device)
                self.attachSinks(device, config)

            # Server
            elif node == "LabSenseServer":
                try:
                    sensors_config = config["Sensors"]
                except KeyError:
                    raise KeyError("No Sensors were specified in LabSenseServer")

                # LabSenseServer has several sensors
                for innerNode, innerConfig in sensors_config.iteritems():
                    if innerNode == "DoorSensor":
                        pass
                    elif innerNode == "MotionSensor":
                        pass
                    else: 
                        raise KeyError("Unrecognized LabSenseServer node: " +
                                       innerNode)
            # Unrecognized
            else:
                raise KeyError("Unrecognized node: " + node)

        print "Number of threads: ", len(self.threads)
        for thread in self.threads:
            thread.daemon = True
            thread.start()

        for thread in self.threads:
            while thread.isAlive():
                thread.join(5)

    def attachSinks(self, device, device_config):
        """ Attaches sinks to devices based on configuration file. """
        for sink in ["SensorAct", "Cosm", "Stdout"]:
            if device_config[sink]:
                interval = device_config[sink + "Interval"]
                queue = Queue.Queue()
                device.attach(queue)
                dataSink = DataSink.DataSink.dataSinkFactory(sink, config, queue, interval)
                dataSink.registerDevice(device_config["name"])
                self.threads.append(dataSink)

if __name__ == "__main__":

    # Read configuration
    config = configReader.config
    main = LabSenseMain(config)
    main.run()



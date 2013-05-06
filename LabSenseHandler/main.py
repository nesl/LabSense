import argparse                             # For parsing command line arguments
import sys                                  # For importing from project directory
import os                                   # For importing from project directory
import Queue                                # For communicating between datasinks and devices
#import threading                            # For making device communication threads
import subprocess                           # For launching each device's processes
import logging                              # For logging each of the devices
import time                                 # For waiting between syncing stdout's of device processes
import configReader                         # For reading the configuration

import fcntl

class LabSenseMain(object):

    class DeviceClass(object):
        """ Stores a device's name, process, and logger """
        def __init__(self, name, device_type, process, logger, queue):
            self.name = name
            self.device_type = device_type
            self.process = process
            self.logger = logger
            self.queue = queue

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configReader.readConfiguration(config_file)
        self.running_devices = []

        # Set up logging for debugging
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",\
                level=logging.DEBUG)

    def startDevices(self):
        """ Parse devices in Configuration file """
        for device, config in self.config.iteritems():
            # Sinks
            if device == "SensorAct":
                required_fields = ["IP", "PORT", "API_KEY"]
                for field in required_fields:
                    if not config[field]:
                        sys.exit("SensorAct requires the field " + field)

            elif device == "Cosm":
                required_fields = ["API_KEY", "user_name"]
                for field in required_fields:
                    if not config[field]:
                        sys.exit("Cosm requires the field " + field)

            elif device == "Stdout":
                pass

            # Devices 
            elif device in ["Eaton", "Veris", "Raritan", "SmartSwitch",
                          "LightSensor", "TemperatureSensor", "LabSenseServer"]:
                # For each device, start the device process, create a logger for
                # it, and store into running_devices list.
                process = self.__startDevice(device, config["name"])
                name = config["name"]
                logger = logging.getLogger(name)
                logger.propagate = False            # Don't propagate to console
                formatter = logging.Formatter("%(asctime)s %(message)s")
                filehandler = logging.FileHandler("logs/%s.log" % name, "w")
                filehandler.setLevel(logging.DEBUG)
                filehandler.setFormatter(formatter)
                logger.addHandler(filehandler)
                device_queue = Queue.Queue()
                device_class = self.DeviceClass(config["name"], device, process, logger, device_queue)
                self.running_devices.append(device_class)

            # Unrecognized
            else:
                raise KeyError("Unrecognized device: " + device)

    def monitorDevices(self, timeout):
        """ This variable helps increase timeout for everytime the error
        persists"""

        i = 0

        while True:
            for device in self.running_devices:
                device_process = device.process.poll()

                # If child process dies, restart it
                if device_process is not None:
                    print "CHILD DIED"
                    print "linearly increasing timeout = "+str(i)
                    i = i+5
                    if i == 500:
                        i = 0
                        print "timeout backoff at 500 seconds, resetting to 0"
                    device.process = self.__startDevice(device.device_type, device.name)

                std_out_line = None
                std_err_line = None
                try:
                    std_out_line = device.process.stdout.read()
                    std_err_line = device.process.stderr.read()
                except IOError:
                    pass

                if std_out_line:
                    device.logger.debug(std_out_line)

                if std_err_line:
                    device.logger.debug(std_err_line)
                
                time.sleep(timeout+i) 

    """ Helper functions called within LabSenseMain class """

    def __startDevice(self, device, devicename):
        """ Starts the device's process """

        # Create device arguments for running with python
        args = ["python"]

        # First argument is the python file to run
        # This is the Device directory + path to the device
        device_directory = os.path.join(os.path.dirname(__file__),\
                                    "../Devices")
        device_path = self.__getDevicePath(device)
        device_path = os.path.join(device_directory, device_path)
        args.append(device_path)

        # Append the config file path
        config_path = os.path.abspath(self.config_file)
        args.append(config_path)

        # Start the process
        # SmartSwitch, LightSensor, and TemperatureSensor need device name
        if device in ["SmartSwitch", "LightSensor", "TemperatureSensor"]:
            args.append(device)

        # Append the name of the device
        args.append(devicename)
            
        process = self.__startProcess(args)

        # Make the stdout and stderr nonblocking
        fcntl.fcntl(process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(process.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

        return process

    def __getDevicePath(self, device):
        """ Gets the path for the given device """
        name = None
        if device == "LabSenseServer":
            device_path = "LabSenseServer/server.py"

        elif device == "Eaton":
            device_path = "LabSenseModbus/Eaton/EatonDevice.py"

        elif device == "Veris":
            device_path = "LabSenseModbus/Veris/VerisDevice.py"

        elif device == "Raritan":
            device_path = "LabSenseRaritan/RaritanDevice.py"

        elif device in ["SmartSwitch", "LightSensor", "TemperatureSensor"]:
            device_path = "LabSenseZwave/ZwaveDevice.py"
        else: 
            raise KeyError("No device named " + device)

        return device_path


    def __startProcess(self, args):
        """ Starts a new process with the given arguments """

        print "Starting process: " + " ".join(args)

        process = subprocess.Popen(args, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process

if __name__ == "__main__":

    # Get configuration file from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Configuration File, defaults to\
                        config.json", default="config.json")
    args = parser.parse_args()

    # Read configuration and run LabSense
    main = LabSenseMain(args.config)
    main.startDevices()
    main.monitorDevices(1)

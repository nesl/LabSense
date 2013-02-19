import httplib, urllib          # For connecting to VPDS Server
import argparse                 # For Parsing Command Line Arguments
import user                     # Specifies the API_KEY
import json                     # For JSON sent to/from VPDS Server
import subprocess               # For launching device processes
import os                       # For getting directories of device processes
import logging                  # For logging the output of each device process
import time                     # For sleeping between each check that
                                    # processes are still running


import DevicesToRegister.raritan as Raritan
import DevicesToRegister.veris as Veris
import DevicesToRegister.zwaveDoorWindow as ZwaveDoorWindow
import DevicesToRegister.zwaveHsm as ZwaveHsm
import DevicesToRegister.eaton as Eaton

from device import DeviceClass      # For combining device properties into one
                                    # class

class LabSenseHandler:

    def __init__(self, config_file):
        self.IP = "1"
        self.PORT = "1"

        self.devices = [];
        self.SensorAct = {}
        self.Cosm = {}
        self.Eaton = {}

        # List of Devices
        self.running_devices = []
        
        # Set up logging
        logging.basicConfig(format="%(asctime)s %(message)s",\
                level=logging.DEBUG)

        self.config_file = config_file
        self.API_KEY = user.API_KEY

        self.headers = { "Content-type": "application/json",
                         "Accept": "text/plain" }


    """ Connection functions """

    def connect(self):

        ip = self.SensorAct["IP"]
        port = self.SensorAct["PORT"]

        self.connection = httplib.HTTPConnection(ip + ":" + port)

        print "Successfully connected to " + ip + ": " + port

    #def registerUser(self, username, password, email):
        #body = '{ "username": "%s", "password": "%s", "email": "%s" }' % username, password, email

        #self.connection.request("POST", "/user/register", body, headers)

        #self.getResponse()


    def closeConnection(self):
        self.connection.close()

    """ Multiple device level Calls """

    def listDevices(self):
        body = '{ "secretkey": "' + self.API_KEY + '"}'
        self.connection.request("POST", "/device/list", body, self.headers)

        self.getResponse()

    def addDevices(self):
        print "Adding all devices"

        #devices = ["Raritan", "Veris", "ZwaveDoorWindow", "ZwaveHsm", "Eaton"]
        for device in self.devices:
            self.addDevice(device)

    def deleteDevices(self):
        print "Deleting all devices"

        devices = ["NESL_Raritan", "NESL_Veris", "NESL_ZwaveDoorWindow", "NESL_ZwaveHsm", "NESL_Eaton"]
        for device in devices:
            self.deleteDevice(device)

    def startDevices(self):
        for device in self.devices:
            self.startDevice(device)

    def monitorDevices(self, timeout):

        while True:
            for device  in self.running_devices:
                device.process.poll()
                std_line = device.process.stdout.readline()
                std_err_line = device.process.stderr.readline()

                #print "Std_err_line: " + std_err_line
                
                if std_line:
                    device.logger.debug(std_line)
                
                #if std_err_line:
                    #device.logger.debug(std_err_line)

            time.sleep(timeout)

    """ Single Device level Calls """
    def addDevice(self, name):
        print "Adding device " + name

        if name == "Raritan":
            deviceprofile = Raritan.body

        elif name == "Veris":
            deviceprofile = Veris.body

        elif name == "ZwaveDoorWindow":
            deviceprofile = ZwaveDoorWindow.body

        elif name == "ZwaveHsm":
            deviceprofile = ZwaveHsm.body

        elif name == "Eaton":
            deviceprofile = Eaton.body

        else:
            return False

        body = '{ "secretkey": "' + self.API_KEY + '", ' + deviceprofile + '}'
        self.connection.request("POST", "/device/add", body, self.headers)

        self.getResponse()

        return True


    def deleteDevice(self, devicename):
        """ Deletes device with the devicename given 
            Note: Currently SensorAct api is not working, so device is not
            deleted. """
        body = '{ "secretkey": "' + self.API_KEY + '", "devicename": "' + devicename + '"}'
        print body
        self.connection.request("POST", "/device/delete", body, self.headers)

        self.getResponse()

    def startDevice(self, device_name):

        print "Running " + device_name
        if device_name == "Eaton":
            process = self.startEaton()
            logger = logging.getLogger(device_name)
            logger.addHandler(logging.FileHandler("logs/" + device_name + ".log"))
            device = DeviceClass(device_name, process, logger)
            self.running_devices.append(device)

        elif device_name == "Raritan":
            pass
        elif device_name == "Veris":
            pass
        elif device_name == "ZwaveDoorWindow":
            pass
        elif device_name == "ZwaveHsm":
            pass
        else:
            raise KeyError(key + " is not a recognized device.")


    """ startDevice Helper Functions for starting device processes """
    def startEaton(self):
        path = []
        path.append(os.path.join(os.path.dirname(__file__),\
            "../LabSenseModbus/TCPModbusClient"))
        path.append("read")
        path.append("eaton")
        path.append("-SensorActIp")
        path.append(self.SensorAct["IP"])
        path.append("-SensorActPort")
        path.append(self.SensorAct["PORT"])
        path.append("-SensorActApi_key")
        path.append(self.SensorAct["API_KEY"])

        process = subprocess.Popen(path, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        return process

    """ Helper functions """

    def getResponse(self):

        response = self.connection.getresponse()
        print response.status, response.reason
        data = response.read()
        print data

if __name__ == "__main__":

    # Check arguments for user specified configuration file
    parser = argparse.ArgumentParser()
    parser.add_argument("--f", help="Configuration File, defaults to\
            config.json", default="config.json")
    args = parser.parse_args()

    labSenseHandler = LabSenseHandler(args.f)

    # Read Config file adn connect
    labSenseHandler.readConfiguration()
    labSenseHandler.connect()

    # Add Devices Specified
    labSenseHandler.addDevices()

    labSenseHandler.listDevices()

    # Launch the executables with parameters
    labSenseHandler.startDevices()

    # Monitor the devices (restart when they fail and log)
    labSenseHandler.monitorDevices(1)

    print "Adding a device"
    #labSenseHandler.addDevice("Raritan")

    #labSenseHandler.deleteDevice("NESL_Raritan")

    #labSenseHandler.listDevices()

    #labSenseHandler.addDevices()

    #labSenseHandler.deleteDevices()

    #labSenseHandler.closeConnection()


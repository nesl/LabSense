import httplib, urllib          # For connecting to VPDS Server
import argparse                 # For Parsing Command Line Arguments
import user                     # Specifies the API_KEY
import json                     # For JSON sent to/from VPDS Server

import DevicesToRegister.raritan as Raritan
import DevicesToRegister.veris as Veris
import DevicesToRegister.zwaveDoorWindow as ZwaveDoorWindow
import DevicesToRegister.zwaveHsm as ZwaveHsm

class LabSenseHandler:

    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.API_KEY = user.API_KEY
        self.connect()

        self.headers = { "Content-type": "application/json",
                      "Accept": "text/plain" }


    """ Connection functions """

    def connect(self):

        self.connection = httplib.HTTPConnection(self.IP + ":" + self.PORT)

        print "Successfully connected to " + self.IP + ": " + self.PORT

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

        devices = ["Raritan", "Veris", "ZwaveDoorWindow", "ZwaveHsm"]
        for device in devices:
            self.addDevice(device)

    def deleteDevices(self):
        print "Deleting all devices"

        devices = ["Raritan", "Veris", "ZwaveDoorWindow", "ZwaveHsm"]
        for device in devices:
            self.deleteDevice(device)


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


    """ Helper functions """

    def getResponse(self):

        response = self.connection.getresponse()
        print response.status, response.reason
        data = response.read()
        print data



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("IP", help="IP address of VPDS Server")
    parser.add_argument("PORT", help="PORT of VPDS Server")
    args = parser.parse_args()

    labSenseHandler = LabSenseHandler(args.IP, args.PORT)

    #labSenseHandler.listDevices()

    print "Adding a device"
    #labSenseHandler.addDevice("Raritan")

    #labSenseHandler.deleteDevice("NESL_Raritan")

    #labSenseHandler.listDevices()

    #labSenseHandler.addDevices()

    labSenseHandler.deleteDevices()

    labSenseHandler.closeConnection()

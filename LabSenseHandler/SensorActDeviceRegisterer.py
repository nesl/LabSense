import httplib                  # For connecting to SensorAct
import os                       # For opening json files

from DeviceRegisterer import DeviceRegisterer 

class SensorActDeviceRegisterer(DeviceRegisterer):

    def __init__(self, ip, port, api_key):
        """ SensorAct constructor"""
        self.ip = ip
        self.port = port
        self.api_key = api_key
        self.headers = { "Content-type": "application/json",
                         "Accept": "text/plain" }

    def connect(self):
        """ Connects to SensorAct"""
        self.connection = httplib.HTTPConnection("%s:%s" %(self.ip, self.port)) 

    def getResponse(self):
        response = self.connection.getresponse()
        print response.status, response.reason
        data = response.read()
        return data

    def getDeviceJson(self, device):
        """ Looks in DevicesToRegister
        directory for SensorAct json for
        registerinregistering the device."""

        device_file_path = os.path.abspath(os.path.dirname(__file__)) + "/DevicesToRegister/%s.json" % device
        device_file = open(device_file_path)
        return device_file.read()

    def getRegisteredDevices(self):
        """ Gets the registered devices on SensorAct """
        self.connect()
        body = '{"secretkey": "%s"}' % self.api_key
        self.connection.request("POST", "/device/list", body, self.headers )
        data = self.getResponse()
        print data

    def registerDevice(self, device, device_config):
        """ Registers a device to SensorAct """

        # Get SensorAct registration json for device
        device_json = self.getDeviceJson(device)

        # Replace the variables with ones in the configuration
        device_profile = device_json % (device_config["name"],
                                        device_config["location"],
                                        device_config["IP"],
                                        device_config["latitude"],
                                        device_config["longitude"])







if __name__ == '__main__':
    # Read the configuration
    import configReader
    config = configReader.config

    # Initialize the registerer
    saRegisterer = SensorActDeviceRegisterer(config["SensorAct"]["IP"],
                                             config["SensorAct"]["PORT"],
                                             config["SensorAct"]["API_KEY"])

    # List Devices
    saRegisterer.getRegisteredDevices()



    # Register Devices
    #saRegisterer.registerDevice("Eaton", config["Eaton"])

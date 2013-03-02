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
        self.connection.close()
        return data

    def getDeviceJson(self, device):
        """ Looks in DevicesToRegister
        directory for SensorAct json for
        registerinregistering the device."""

        device_file_path = os.path.abspath(os.path.dirname(__file__)) + "/DevicesToRegister/%s.json" % device
        device_file = open(device_file_path)
        return device_file.read()

    def getRegisteredDevices(self):
        """ Gets the registered devices on SensorAct and puts them into self.devices """
        self.connect()
        body = '{"secretkey": "%s"}' % self.api_key
        self.connection.request("POST", "/device/list", body, self.headers )
        data = self.getResponse()
        print "Data: %s" %data

    def getDeviceProfile(self, device, device_config):
        """ Gets the device profile and fills it with
        the configuration options """

        # Get SensorAct registration json for device
        device_json = self.getDeviceJson(device)

        # Replace the variables with ones in the configuration
        device_profile = device_json % (self.api_key,
                                        device_config["name"],
                                        device_config["location"],
                                        device_config["IP"],
                                        device_config["latitude"],
                                        device_config["longitude"])
        return device_profile

    def registerDevice(self, device, device_config):
        """ Registers a device to SensorAct """

        # Get the device profile
        device_profile = self.getDeviceProfile(device, device_config)
        print "Device profile: %s" % device_profile

        # Register the Device to SensorAct
        self.connect()
        self.connection.request("POST", 
                                "/device/add",
                                device_profile, 
                                self.headers)
        data = self.getResponse()
        print "Response: %s" % data


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
    devices = ["Eaton", "Raritan"]
    for device in devices:
        saRegisterer.registerDevice(device, config[device])

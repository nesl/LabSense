import httplib                  # For connecting to SensorAct
import os                       # For opening json files
import json                     # For reading json

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

    def deleteDevice(self, device):
        """ Deletes the device from SensorAct """
        body = '{"secretkey": "%s", "devicename": "%s"}' % (self.api_key, device)
        self.connection.request("POST", "/device/delete", body, self.headers )
        data = self.getResponse()
        print "Data: %s" %data

    def getDeviceJson(self, device):
        """ Looks in DevicesToRegister directory for SensorAct json for
        registerinregistering the device."""

        device_file_path = os.path.abspath(os.path.dirname(__file__)) + "/DevicesToRegister/%s.json" % device
        device_file = open(device_file_path)
        device_json = json.load(device_file)
        device_json = self.__convert(device_json)
        return device_json

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

        # Fill in deviceprofile with configuration options
        device_json["secretkey"] = self.api_key
        device_json["deviceprofile"]["devicename"] = device_config["name"]
        device_json["deviceprofile"]["location"] = device_config["location"]
        device_json["deviceprofile"]["IP"] = device_config["IP"]
        device_json["deviceprofile"]["latitude"] = device_config["latitude"]
        device_json["deviceprofile"]["longitude"] = device_config["longitude"]

        samplingperiod = device_config["sinterval"]
        for sensors in device_json["deviceprofile"]["sensors"]:
            for channel in sensors["channels"]:
                channel["samplingperiod"] = samplingperiod

        return json.dumps(device_json)

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

    """ Helper functions """

    def __convert(self, unicode_dict):
        """ When reading in a JSON file into a dictionary, the elements are read in as unicode. This function converts it to strings. """

        if isinstance(unicode_dict, dict):
            return {self.__convert(key): self.__convert(value) for key, value in unicode_dict.iteritems()}
        elif isinstance(unicode_dict, list):
            return [self.__convert(element) for element in unicode_dict]
        elif isinstance(unicode_dict, unicode):
            return unicode_dict.encode('utf-8')
        else:
            return unicode_dict 


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
    #devices = ["Eaton", "Raritan", "Veris"]
    #devices = ["SmartSwitch"]
    #devices = ["LightSensor", "TemperatureSensor"]
    #devices = ["TemperatureSensor"]
    #devices = ["DoorSensor", "MotionSensor"]
    devices = ["LabSenseServer"]

    #device_names = ["NESL_Eaton", "NESL_Raritan"]
    #for device_name in device_names:
        #saRegisterer.deleteDevice(device_name)
        
    for device in devices:
        if device == "LabSenseServer":
            # LabSenseServer has several sensors
            # (DoorSensor and MotionSensor)
            for sensorname, sensorconfig in config[device]["Sensors"].iteritems():
                saRegisterer.registerDevice(sensorname,
                                            sensorconfig)
        else:
            # All others have one type of sensor
            saRegisterer.registerDevice(device, config[device])

    # List Devices
    saRegisterer.getRegisteredDevices()

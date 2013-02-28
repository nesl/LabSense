from DeviceRegisterer import DeviceRegisterer 

class SensorActDeviceRegisterer(DeviceRegisterer):

    def __init__(self):
        """ SensorAct constructor"""
        pass

    def registerDevice(device, device_config):

        #try:
        device_file = open(device + ".json")
        #except Exception, e:
            #raise e

if __name__ == '__main__':
    saRegisterer = SensorActDeviceRegisterer()
    saRegisterer.registerDevice("Eaton")




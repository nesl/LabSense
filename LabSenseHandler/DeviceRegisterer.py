class DeviceRegisterer(object):
    """ Registers Devices to SensorAct and Cosm """

    def getRegisteredDevices(self):
        """ Gets the registered devices """
        raise NotImplementedError("All inherited classes of DeviceRegisterer must implement getRegisteredDevices.")

    def registerDevice(device, device_config):
        """ Registers a device to SensorAct. """
        raise NotImplementedError("All inherited classes of DeviceRegisterer must implement registerDevice.")

        #if device == "Eaton":
            #pass
        #elif device == "Veris":
            #pass
        #elif device == "Raritan":
            #pass
        #elif device == "SmartSwitch":
            #pass
        #elif device == "LightSensor":
            #pass
        #elif device == "TemperatureSensor":
            #pass
        #elif device == "DoorSensor":
            #pass
        #elif device == "MotionSensor":
            #pass
        #else:
            #raise KeyError(str(device) + " is not a \
                           #recognized device.")


class DeviceRegisterer(object):
    """ Registers Devices to SensorAct and Cosm """

    def getRegisteredDevices(self):
        """ Gets the registered devices """
        raise NotImplementedError("All inherited classes of DeviceRegisterer must implement getRegisteredDevices.")

    def registerDevice(device, device_config):
        """ Registers a device to SensorAct. """
        raise NotImplementedError("All inherited classes of DeviceRegisterer must implement registerDevice.")

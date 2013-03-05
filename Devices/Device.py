import time                                 # For sleeping between data transfers
import threading                            # For threading datasinks

""" Represents a generic device. The Observer pattern is used to attach
different loggers to each device. """
class Device(threading.Thread):

    def __init__(self, sinterval):
        """ Initializes device with the sampling interval. """
        threading.Thread.__init__(self)
        self.queues = []
        self.sinterval = float(sinterval)

    def deviceFactory(device_type, name, ip, port,
                      channels, sinterval):
        import LabSenseModbus.Eaton.EatonDevice as EatonDevice
        import LabSenseModbus.Veris.VerisDevice as VerisDevice
        import LabSenseZwave.ZwaveDevice as ZwaveDevice
        import LabSenseRaritan.RaritanDevice as RaritanDevice

        if device_type == "Eaton":
            return EatonDevice.EatonDevice(name, 
                                           ip,
                                           port,
                                           channels,
                                           sinterval)
        elif device_type == "Veris":
            return VerisDevice.VerisDevice(name,
                                           ip,
                                           port,
                                           channels,
                                           sinterval)
        elif device_type == "Raritan":
            return RaritanDevice.RaritanDevice(name,
                                           ip,
                                           port,
                                           channels,
                                           sinterval)
        elif device_type in ["SmartSwitch",
                             "LightSensor",
                             "TemperatureSensor"]:
            return ZwaveDevice.ZwaveDevice(device_type,
                                           name,
                                           ip,
                                           port,
                                           channels,
                                           sinterval)
        else:
            raise KeyError("Unrecognized Device Name " +
                           device_type)
    # Make deviceFactory static so Device does not have to be instantiated
    # to run
    deviceFactory = staticmethod(deviceFactory)

    def attach(self, queue):
        if not queue in self.queues:
            self.queues.append(queue)

    def detach(self, queue):
        try:
            self.queues.remove(queue)
        except ValueError:
            pass

    def notify(self, data):
        if data:
            for queue in self.queues:
                queue.put(data)

    def getData(self):
        data = self.client.getData()
        if data:
            self.notify(data)
            return data

    def run(self):
        print "Starting Device"
        while True:
            self.getData()
            time.sleep(self.sinterval)

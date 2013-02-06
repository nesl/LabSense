from DataSink import DataSink

class StdoutSink(DataSink):

    def __init__(self, config, queue, interval):
        super(StdoutSink, self).__init__(interval, queue) 

    def registerDevice(self, name):
        if device_name not in self.devices:
            self.devices.append(device_name)

    def update(self, data):
        print "StdoutSink data: " + str(data)

from DataSink import DataSink

class StdoutSink(DataSink):

    def __init__(self):
        super(StdoutSink, self).__init__()

    def registerDevice(self, device_name, name):
        if device_name not in self.devices:
            self.devices.append(device_name)
        

    def update(self, data):
        print "StdoutSink data: " + str(data)


import DataSink

class FileSink(DataSink.DataSink):

    def __init__(self, config, queue, interval):
        super(FileSink, self).__init__(config, queue, interval)

    def registerDevice(self, name):
        if device_name not in self.devices:
            self.devices.append(device_name)
            self.device_file = open(name + "_log.txt", "w")

    def update(self, data):
        self.device_file.write(data)

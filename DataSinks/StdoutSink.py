import DataSink

class StdoutSink(DataSink.DataSink):

    def __init__(self, config, queue, interval):
        super(StdoutSink, self).__init__(config, queue, interval) 

    def registerDevice(self, devicename, config):
        """ Stdout does not require any registering """
        pass

    def update(self, data):
        print "StdoutSink data: " + str(data)

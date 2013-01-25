from DataSink import DataSink

class StdoutSink(DataSink):

    def __init__(self):
        super(StdoutSink, self).__init__()

    def update(self, data):
        print "StdoutSink data: " + str(data)


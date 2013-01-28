class DataSink(object):
    
    def __init__(self):
        self.devices = []

    def update(self, data):
        raise NotImplementedError("DataSink is an abstract class. sendData must\
                be implemented by classes that inherit from DataSink.")


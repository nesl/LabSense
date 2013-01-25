""" Represents a generic device. The Observer pattern is used to attach
different loggers to each device. """
class Device(object):

    def __init__(self):
        self.observers = []

    def attach(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)

    def getData(self):
        raise NotImplementedError("Device class is an abstract class.")

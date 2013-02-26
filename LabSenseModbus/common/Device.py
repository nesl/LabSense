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

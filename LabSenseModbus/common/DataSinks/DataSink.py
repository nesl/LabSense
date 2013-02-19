import time                                 # For sleeping between data transfers
import threading                            # For threading datasinks

class DataSink(threading.Thread):
    
    def __init__(self, interval, queue):
        threading.Thread.__init__(self)
        self.interval = float(interval)
        self.devices = []
        self.queue = queue

        # Default behavior for Datasinks is not to batch.
        self.batch = False 

    def run(self):
        print "Starting DataSink"
        while True:

            if not self.queue.empty():
                data = self.queue.get()
                start_time = time.time()
                self.update(data)
                end_time = time.time()
                print "update elapsed time: %r, with %d items in queue. " % (end_time - start_time, self.queue.qsize())
            else:
                print "Queue was empty"

            time.sleep(self.interval)

    """ Functions child classes must implement """

    def update(self, data):
        raise NotImplementedError("DataSink is an abstract class. sendData must\
                be implemented by classes that inherit from DataSink.")

    def __registerDevice(self, device_name, name):
        raise NotImplementedError("DataSink is an abstract class.\
                RegisterDevice must be implemented by classes that inherit\
                from DataSink.")

